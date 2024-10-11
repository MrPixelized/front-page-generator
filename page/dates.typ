#import "@preview/cetz:0.2.2": canvas, draw, plot

#let parse-date(iso-date) = {
  let (iso-date, ..rest) = iso-date.split(".")
  if "T" not in iso-date {
    let (year, month, day) = iso-date.split("-").map(int)
    return datetime(year: year, month: month, day: day)
  } else {
    let (date, time) = iso-date.split("T")
    let (hour, minute, ..rest) = time.split(":").map(int)
    let (year, month, day) = date.split("-").map(int)

    return datetime(year: year, month: month, day: day, hour: hour, minute:
    minute, second: 0)
  }
}

#let is-day-after(a, b) = {
  if a.year() == b.year() and a.ordinal() - b.ordinal() == 1 {
    return true
  }

  if a.month() == 12 and a.day() == 31 and b.month() == 1 and b.day() == 1 and a.year() + 1 == b.year() {
    return true
  }

  return false
}

#let display-day(date) = {
  if date == none {
    return
  }

  if type(date) != datetime {
    date = parse-date(date)
  }

  if date == datetime.today() {
    return [Today]
  } else if is-day-after(date, datetime.today()) {
    return [Tomorrow]
  } else {
    return date.display("[weekday]")
  }
}

#let morning-of(date) = datetime(
  year: date.year(), month: date.month(), day: date.day(),
  hour: 5, minute: 0, second: 0
)

#let night-of(date) = datetime(
  year: date.year(), month: date.month(), day: date.day(),
  hour: 23, minute: 0, second: 0
)
