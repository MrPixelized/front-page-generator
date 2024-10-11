import json
import requests
import feedparser
import dateutil
from dateutil.parser import isoparse
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from collections import defaultdict
from wmo_codes import wmo_codes
from typing import List, Dict, TypeVar, TypedDict, Callable
from dataclasses import dataclass, asdict, field, is_dataclass
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from argparse import ArgumentParser

K = TypeVar("K")
T = TypeVar("T")


def filter_dict_keys(d: dict, condition: Callable):
    return {k: v for k, v in d.items() if condition(k)}


@dataclass
class Article:
    title: str
    summary: str
    url: str
    timestamp: datetime

    def __post_init__(self):
        self.summary = parse_html(self.summary)


@dataclass
class Location:
    latitude: float
    longitude: float
    timezone: str
    name: str

    def __str__(self):
        return f"{self.name} ({self.latitude},{self.longitude})"

    @classmethod
    def fetch(cls, location: str | None = None): # -> Location:
        # If no location specified, fetch it using IP
        if location == None:
            data = json_from_url("https://ipinfo.io")
            return Location(*data["loc"].split(","),
                            timezone=data["timezone"],
                            name=f"{data['city']}, {data['region']}, {data['country']}")

        # Maybe the location is already a lat, lon[, name] pair/triple
        try:
            lat, lon, timezone, *location = location.split(",")
            location = ",".join(location)
            return Location(float(lat), float(lon), timezone=timezone, name=location)
        except (ValueError, TypeError):
            pass

        # Otherwise, look the location up using a geocoding API
        data = json_from_url("https://geocoding-api.open-meteo.com/v1/search",
                             name=location, count=1)
        data = data["results"][0]

        return cls(
            data["latitude"],
            data["longitude"],
            timezone=data["timezone"],
            name=f"{data['name']}, {data['admin1']}, {data['country_code']}"
        )


@dataclass(kw_only=True)
class BaseWeatherDatum:
    location: Location
    timestamp: datetime
    wmo_code: int
    statement: dict = field(default_factory=dict)

    def __post_init__(self):
        if not hasattr(self, "temperature") or self.temperature is None:
            self.temperature = self.temperature_max

        if not hasattr(self, "statement") or not self.statement:
            self.gen_statement()

    def gen_statement(self):
        """ Take weather stats at a specific point in time and return an
        English-language statement about them """

        daytime = "day"
        if hasattr(self, "sunrise") and hasattr(self, "sunset"):
            if self.timestamp < self.sunrise or self.timestamp > self.sunset:
                daytime = "night"

        self.statement = {}
        self.statement["wmo"] = wmo_codes[self.wmo_code][daytime]

        if self.temperature > 25:
            self.statement["temperature"] = "hot"
        elif self.temperature > 20:
            self.statement["temperature"] = "warm"
        elif self.temperature > 15:
            self.statement["temperature"] = "moderate"
        elif self.temperature > 10:
            self.statement["temperature"] = "chilly"
        elif self.temperature > 5:
            self.statement["temperature"] = "cold"


@dataclass
class DailyWeatherDatum(BaseWeatherDatum):
    precipitation_probability: float
    #  precipitation: float
    temperature_max: float
    temperature_min: float
    uv_index: float
    sunshine_duration: timedelta
    sunrise: datetime
    sunset: datetime
    #  cloud_cover: int

    @classmethod
    def from_open_meteo_data(cls, data, location):
        for k in list(data.keys()):
            if "_2m" in k:
                data[k.replace("_2m", "")] = data.pop(k)

        data["wmo_code"] = data.pop("weather_code")
        data["timestamp"] = isoparse(data.pop("time"))
        data["uv_index"] = data.pop("uv_index_max")
        data["precipitation_probability"] = data.pop("precipitation_probability_max")
        data["sunrise"] = isoparse(data["sunrise"])
        data["sunset"] = isoparse(data["sunset"])

        return cls(location=location, **data)


@dataclass
class HourlyWeatherDatum(BaseWeatherDatum):
    precipitation_probability: float
    precipitation: float
    temperature: float
    sunshine_duration: timedelta
    cloud_cover: int

    @classmethod
    def from_open_meteo_data(cls, data, location):
        for k in list(data.keys()):
            if k.endswith("_2m"):
                data[k.removesuffix("_2m")] = data.pop(k)

        data["wmo_code"] = data.pop("weather_code")
        data["timestamp"] = isoparse(data.pop("time"))

        return cls(location=location, **data)


@dataclass
class DailyAggregateAndHourlyWeather:
    aggregate: DailyWeatherDatum
    hourly: dict[datetime, HourlyWeatherDatum]


@dataclass
class WeatherForecast:
    location: Location
    forecast_days: 1
    by_date: dict[date, DailyAggregateAndHourlyWeather] = field(default_factory=dict)
    hourly: dict[datetime, HourlyWeatherDatum] = field(default_factory=dict)
    daily: dict[date, DailyWeatherDatum] = field(default_factory=dict)

    hour_data_points = [
        "temperature_2m",
        "sunshine_duration",
        "precipitation_probability",
        "precipitation",
        "cloud_cover",
        "weather_code",
    ]
    day_data_points = [
        "temperature_2m_max",
        "temperature_2m_min",
        "sunshine_duration",
        "sunrise",
        "sunset",
        "weather_code",
        "uv_index_max",
        "precipitation_probability_max",
    ]

    def __post_init__(self):
        self.refresh()

    def refresh(self):
        """ Return the weather at the location for the given number of forecast
        days, grouped by date """

        data = json_from_url("https://api.open-meteo.com/v1/forecast",
                             #  current=self.hour_data_points,
                             hourly=",".join(self.hour_data_points),
                             daily=",".join(self.day_data_points),
                             forecast_days=self.forecast_days,
                             **asdict(self.location))
        
        hourly = [HourlyWeatherDatum.from_open_meteo_data(d, self.location)
                  for d in transpose_dict_lists(data["hourly"])]
        daily = [DailyWeatherDatum.from_open_meteo_data(d, self.location)
                 for d in transpose_dict_lists(data["daily"])]

        self.hourly = {datum.timestamp: datum for datum in hourly}
        self.daily = {datum.timestamp.date(): datum for datum in daily}
        self.by_date = {date:
            DailyAggregateAndHourlyWeather(
                aggregate=self.daily[date],
                hourly=filter_dict_keys(self.hourly, lambda k: k.date() == date)
            )
            for date in self.daily.keys()}


def parse_html(html):
    # https://stackoverflow.com/a/66690657
    elem = BeautifulSoup(html, features="html.parser")
    text = ""
    for e in elem.descendants:
        if isinstance(e, str):
            text += e#.strip()
        elif e.name in ["br", "p", "h1", "h2", "h3", "h4", "tr", "th", "div"]:
            if not text.endswith("\n\n"):
                text += "\n"
        elif e.name == "li":
            text += "\n- "
    return text.strip()


def transpose_dict_lists(d: Dict[K, List[T]]) -> List[Dict[K, T]]:
    """ "Transpose" a dictionary of lists, returning a list of dictionaries,
    each n-th item in the list containing the n-th item in the original list at
    dict[k] for each k in the dict. Consumes the original lists. """
    l = []

    while any(d.values()):
        l.append({k: d[k].pop(0) for k in d if d[k]})

    return l


def json_from_url(url, **params):
    req = requests.PreparedRequest()
    req.prepare_url(url, params)

    return json.loads(requests.get(req.url).content)


def fetch_rss_articles(url: str) -> List[Article]:
    data = feedparser.parse(url)

    articles = []

    for entry in data.entries:
        articles.append(Article(
            title=entry["title"],
            summary=entry["summary"],
            url=entry["link"],
            timestamp=datetime(*entry["published_parsed"][:5]),
        ))

    return articles

fetch_articles = fetch_rss_articles


def asdictify(d) -> dict:
    if is_dataclass(d):
        return asdictify(asdict(d))

    if isinstance(d, list):
        return list(map(asdictify, d))

    if isinstance(d, dict):
        return {k: asdictify(v) for k, v in d.items()}

    return d


def seriablize(d) -> dict:
    if isinstance(d, list):
        return list(map(seriablize, d))

    if isinstance(d, dict):
        return {seriablize(k): seriablize(v) for k, v in d.items()}

    if isinstance(d, datetime) or isinstance(d, date):
        return d.isoformat()

    return d


class FrontPage:
    def __init__(self, locations=None, rss_feeds=[], forecast_days=1):
        if locations is None:
            locations = [None]

        self.locations = list(map(Location.fetch, locations))
        self.feeds = rss_feeds
        self.forecast_days = forecast_days

        self.refresh()

    def refresh(self):
        self.refresh_time = datetime.now()
        self.weather = {
            str(location): WeatherForecast(location, self.forecast_days) for location in self.locations
        }
        self.news = sum(map(list, zip(*map(fetch_articles, self.feeds))), [])

    def to_json(self):
        return json.dumps(seriablize(asdictify({
            "timestamp": self.refresh_time,
            "weather": {str(k): v for k, v in self.weather.items()},
            "news": self.news,
       })))


def main(**args):
    print(FrontPage(**args).to_json())


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="fpg",
        description="Generates a JSON object containing information that you might want to have on a front page",
    )

    parser.add_argument("-l", "--locations", type=str, action="extend", nargs="*", default=None)
    parser.add_argument("-f", "--forecast-days", type=int, default=1)
    parser.add_argument("-r", "--rss-feeds", type=str, action="extend", nargs="*", default=[])

    args = parser.parse_args()

    main(*args._get_args(), **dict(args._get_kwargs()))
