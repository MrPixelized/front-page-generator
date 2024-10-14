from util import *
from icalendar import Calendar
from dataclasses import dataclass
from pathlib import Path
import recurring_ical_events 


@dataclass
class Quote:
    text: str
    author: str | None = None

    @classmethod
    def fetch_quote(cls):
        quote = json_from_url("https://api.forismatic.com/api/1.0/POST?method=getQuote&format=json&lang=en")

        return cls(
            text=quote["quoteText"],
            author=quote.get("quoteAuthor", None),
        )


fetch_quote = Quote.fetch_quote
