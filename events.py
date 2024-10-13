from util import *
from dataclasses import dataclass


@dataclass
class CalendarEvent:
    title: str
    location: str
    description: str
    start_time: datetime
    end_time: datetime

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

fetch_calendar_events = fetch_calendar_events_from_khal
