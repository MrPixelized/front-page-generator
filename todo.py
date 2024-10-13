from util import *
from icalendar import Calendar
from dataclasses import dataclass
from pathlib import Path
import recurring_ical_events 


@dataclass
class Todo:
    title: str
    status: str
    due: str | None = None
    description: str | None = None

    @classmethod
    def from_ical(cls, ical):
        return cls(
            title=str(ical["SUMMARY"]),
            status=str(ical.get("STATUS", "NEEDS-ACTION")),
            due=ical.get("DUE").dt if "DUE" in ical else None,
            description=str(ical.get("DESCRIPTION", None)),
        )

    def __str__(self):
        return json.dumps(asdictify(self))


def fetch_todo_from_vdir(vdir="/home/ischa/.local/share/caldav/"):
    todos = []

    for ical_file in Path(vdir).glob("**/*.ics"):
        with ical_file.open("rb") as f:
            ical = Calendar.from_ical(f.read())
            for todo in ical.walk("VTODO"):
                if todo.get("STATUS", "NEEDS-ACTION") != "COMPLETED":
                    todos.append(todo)

    return [Todo.from_ical(todo) for todo in todos]


fetch_todo = fetch_todo_from_vdir
