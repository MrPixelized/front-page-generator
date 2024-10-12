from util import *
from dataclasses import dataclass
from location import Location
from wmo_codes import wmo_codes


@dataclass(kw_only=True)
class BaseWeatherDatum:
    location: Location
    timestamp: datetime | date
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
        if type(self.timestamp) is datetime:
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

    def __str__(self):
        return (
            f"{self.location} @ {self.timestamp}: " +
            f"{self.statement['wmo']['description']}, " +
            f"{self.statement['temperature']} temperatures"
        )


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
        data["timestamp"] = isoparse(data.pop("time")).date()
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

    def __str__(self):
        return "\n".join(map(str, self.daily.values()))

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
        self.daily = {datum.timestamp: datum for datum in daily}
        self.by_date = {date:
            DailyAggregateAndHourlyWeather(
                aggregate=self.daily[date],
                hourly=filter_dict_keys(self.hourly, lambda k: k.date() == date)
            )
            for date in self.daily.keys()}
