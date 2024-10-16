from util import *
from weather import WeatherForecast
from finance import BalanceSheet, BudgetSheet
from location import Location
from news import fetch_articles
from events import fetch_calendar_events
from todo import fetch_todo
from quote import fetch_quote
import json
from argparse import ArgumentParser


class FrontPage:
    def __init__(self, locations=None, rss_feeds=[], forecast_days=1,
                 vdir=None, hledger_args=[]):
        if locations is None:
            locations = [None]

        self.locations = list(map(Location.fetch, locations))
        self.feeds = rss_feeds
        self.forecast_days = forecast_days
        self.hledger_args = hledger_args
        self.vdir = vdir

        self.refresh()

    def refresh(self):
        self.refresh_time = datetime.now()
        self.weather = [WeatherForecast(location, self.forecast_days)
                        for location in self.locations]
        self.news = sum(map(list, zip(*map(fetch_articles, self.feeds))), [])
        self.balance_sheet = BalanceSheet.from_hledger(*self.hledger_args)
        self.budget_sheet = BudgetSheet.from_hledger(*self.hledger_args)
        self.quote = fetch_quote()

        if self.vdir is None:
            self.events = []
            self.todo = []
        else:
            self.events = fetch_calendar_events(self.vdir)
            self.todo = fetch_todo(self.vdir)

    def to_md(self):
        return (
            "= WEATHER\n" +
            "\n".join(map(str, self.weather.values())) +
            "\n\n" +
            "= NEWS\n" +
            "\n\n".join("== " + str(article) for article in self.news[:6])
        )

    def to_json(self):
        return json.dumps(seriablize(self.to_dict()))

    def to_dict(self):
        return asdictify({
            "timestamp": self.refresh_time,
            "weather": {str(f.location): f for f in self.weather},
            "news": self.news,
            "finance": {
                "balance_sheet": self.balance_sheet,
                "budget_sheet": self.budget_sheet,
            },
            "events": self.events,
            "todo": self.todo,
            "quote": self.quote,
       })


def main(**args):
    print(FrontPage(**args).to_json())
    #  FrontPage(**args).to_json()


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="fpg",
        description="Generates a JSON object containing information that you might want to have on a front page",
    )

    parser.add_argument("-l", "--locations", type=str, action="extend", nargs="*", default=None)
    parser.add_argument("-f", "--forecast-days", type=int, default=1)
    parser.add_argument("-r", "--rss-feeds", type=str, action="extend", nargs="*", default=[])
    parser.add_argument("-v", "--vdir", type=str, default=None)
    parser.add_argument("-H", "--hledger-args", type=str, action="extend", nargs="*", default=[])

    args = parser.parse_args()
    args.hledger_args = [dashify_arg(arg) for arg in args.hledger_args]

    main(*args._get_args(), **dict(args._get_kwargs()))
