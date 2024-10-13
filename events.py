from util import *
from icalendar import Calendar
from dataclasses import dataclass
from pathlib import Path
import recurring_ical_events 


@dataclass
class CalendarEvent:
    title: str
    start_time: datetime
    end_time: datetime | None = None
    location: str | None = None
    description: str | None = None

    @classmethod
    def from_ical(cls, ical):
        return cls(
            title=str(ical["SUMMARY"]),
            start_time=ical["DTSTART"].dt,
            end_time=ical["DTEND"].dt if "DTEND" in ical else None,
        )

    def __str__(self):
        return json.dumps(asdictify(self))


def fetch_calendar_events_from_khal(*args, **kwargs) -> List[CalendarEvent]:
    sep = "\n---\n"
    fields = [
        "title",
        "location",
        "description",
        "start_long",
        "end_long",
    ]
    fmt = (sep.join("{" + f + "}" for f in fields)
           .replace("_", "-")
           .replace("\n", "{nl}")) + "NEXT EVENT"
    data = run("/usr/bin/khal", "list", *args, day_format="", format=fmt, **kwargs)
    data = data.split("NEXT EVENT\n")[:-1]
    data = [dict(zip(fields, event.split(sep))) for event in data]

    for i in data:
        i["start_time"] = datetime.strptime(i.pop("start_long"), "%d/%m/%Y %H:%M")
        i["end_time"] = datetime.strptime(i.pop("end_long"), "%d/%m/%Y %H:%M")

    return [CalendarEvent(**i) for i in data]


def fetch_calendar_events_from_vdir(vdir="/home/ischa/.local/share/caldav/"):
    events = []

    for ical_file in Path(vdir).glob("**/*.ics"):
        with ical_file.open("rb") as f:
            ical = Calendar.from_ical(f.read())
            events.extend(recurring_ical_events.of(ical).at(date.today()))

    return [CalendarEvent.from_ical(event) for event in events]


fetch_calendar_events = fetch_calendar_events_from_vdir
