#import "@preview/cetz:0.2.2": canvas, draw, plot
#import "./dates.typ": *

#let capitalize(s) = upper(s.slice(0, 1)) + s.slice(1)

#let hatching(color: gray.lighten(50%)) = {
  let fg = color.darken(20%)
  let bg = white

  pattern(size: (4pt, 4pt), {
    place(square(size: 5cm, fill: bg))
    place(line(start: (100%, 0%), end: (0%, 100%), stroke: fg))
  })
}

#let slider(pos, left: smallcaps[lo], right: smallcaps[hi], length: 100%) = context {
  canvas(length: length, {
    import draw: *

    let left-size = measure(left).width
    let right-size = measure(right).width

    let padding = 0.5em
    let marker-size = 4.5pt

    line((padding * 2, 0), (rel: (-right-size - left-size, 0), to: (1, 0)),
    name: "line", stroke: 0.5pt)
    mark((rel: (marker-size + 1pt, 0), to: "line.start"), (rel: (1pt, 0), to: "line.end"),
      pos: 100% - pos,
      symbol: "circle",
      fill: white,
      stroke: 0.5pt,
      width: marker-size - 0.5pt,
      length: marker-size,
    )
    set-style(content: (padding: (right: padding)), line: (margin: 0.5em))
    content((rel: (0, 0.75pt), to: "line.start"), left, anchor: "east")
    set-style(content: (padding: (left: padding)), line: (margin: 0.5em))
    content((rel: (0, 0.75pt), to: "line.end"), right, anchor: "west")
  })
}

#let hi-lo(hi: none, lo: none, direction: ttb) = block({
  let columns = if direction == ttb { 3 } else if direction == rtl { 6 }
  let gutter = if direction == ttb { 2pt } else if direction == rtl { 1fr }

  grid(columns: columns, column-gutter: (2pt, 2pt, gutter, 2pt, 2pt), row-gutter: 4pt,
    align: bottom + right,
    text(8pt, smallcaps[hi]), text(12pt, str(hi)),
    text(12pt, sym.degree.c),
    text(8pt, smallcaps[lo]), text(12pt, str(lo)),
    text(12pt, sym.degree.c),
  )
})

#let weather-icon(description, ..args) = {
  let file = "weather-icons/minimalist/" + description + ".svg"

  let data = (read(file)
    .replace("#264b68", black.to-hex())
    .replace("stroke-width:8px", "stroke-width:4px")
  )

  image.decode(data, ..args)
}

#let weather-card(
  date: none, location: none, 
  statement: none,
  hi: none, lo: none,
  icon: none,
  precipitation-probability: none, uv-index: none,
  ..args
) = layout(size => block(..args, {
  let spacing-factor = 6pt
  let icon-size = calc.min(2cm, size.width / 2)

  // Date, location, statement
  box({
    if date != none {
      box(heading(level: 2, smallcaps(display-day(date))))
    }

    if location != none {
      let city = location.name.split(",").first().trim()
      let country = location.name.split(",").last().trim()
      h(1fr)
      // text(8pt)[#city, #country]
      text(8pt, city)
    }
  })

  v(spacing-factor, weak: true)
  text(statement)

  // Icon
  v(icon-size/8, weak: true)
  if icon != none {
    grid(columns: (1fr, auto), align: bottom,
      align(center, box(width: icon-size, icon)),
      hi-lo(hi: hi, lo: lo),
    )
  } else {
    pad(x: 1em, hi-lo(hi: hi, lo: lo, direction: rtl))
  }

  // Sliders
  set text(8pt)
  if precipitation-probability != none {
    strong(smallcaps[Chances of rain])
    v(spacing-factor, weak: true)
    slider(precipitation-probability)
  }

  if uv-index != none {
    strong(smallcaps[UV-index])
    v(spacing-factor, weak: true)
    slider(uv-index)
  }
}))

#let plot-clean(..args) = {
  draw.set-style(axes: (stroke: none, tick: (stroke: none)))
  plot.plot(
    axis-style: "scientific",
    y-tick-step: none,
    x-tick-step: none,
    y-label: none,
    x-label: none,
    ..args
  )
}

#let forecast-graph(data, sunrise: none, sunset: none) = {
  let graph-size = (1, 0.275)
  let icon-width = 28pt
  let sunrise = parse-date(data.aggregate.sunrise)
  let sunset = parse-date(data.aggregate.sunset)

  // Extract timestamps from morning to night
  let timestamps = data.hourly.keys().filter(m => {
    let t = parse-date(m)
    return t > morning-of(t) and t < night-of(t)
  })

  // Create an icon and time for each, use them as ticks
  let tick-timestamps = timestamps.slice(1, -1).chunks(2).map(l => l.at(0))
  let ticks = tick-timestamps.map(t => (parse-date(t).hour(), {
    set text(8pt)
    set align(center)
    stack(dir: ttb,
      box(width: icon-width,
        weather-icon(data.hourly.at(t).statement.wmo.owm_image_description)),
      box(width: icon-width,
        parse-date(t).display("[hour]:[minute]")),
    )
  }))

  let first-hour = parse-date(calc.min(..timestamps)).hour()
  let last-hour = parse-date(calc.max(..timestamps)).hour()

  let min-temp = calc.min(..timestamps.map(t => data.hourly.at(t).temperature))
  let max-temp = calc.max(..timestamps.map(t => data.hourly.at(t).temperature))

  box(width: 100%, {
    canvas(length: 100%, {
      // Astronomy
      plot-clean(size: graph-size, y-min: 0, y-max: 1, name: "astro", {
        let sunrise = sunrise.hour() + sunrise.minute() / 60
        let sunset = sunset.hour() + sunset.minute() / 60

        let noon = (sunset + sunrise) / 2

        plot.add(
          style: (stroke: 0pt),
          (
            (calc.min(..timestamps.map(parse-date).map(t => t.hour())), 0),
            (calc.max(..timestamps.map(parse-date).map(t => t.hour())), 0),
          )
        )

        plot.add-anchor("sunrise", (sunrise, 0))
        plot.add-anchor("sunset", (sunset, 0))
        plot.add-anchor("noon", (noon, (sunset - sunrise) / 22))
        plot.add-anchor("now-bottom", (10, 0))
        plot.add-anchor("now-top", (10, 1))
      })

      draw.intersections("sun", {
        draw.hobby("astro.sunrise", "astro.noon", "astro.sunset",
          stroke: gray.lighten(33%),
          // stroke: gradient.linear(red.darken(20%), orange, yellow, ..(blue.lighten(70%),)*4, dir: btt),
        )
        draw.hide(draw.line("astro.now-bottom", "astro.now-top", name: "now"))
      })

      for (t, anchor) in ((sunrise, "astro.sunrise"), (sunset, "astro.sunset")) {
        draw.content(anchor, {
          set text(6pt, gray.darken(33%))
          v(2pt)
          t.display("[hour]:[minute]")
        }, anchor: "north")
      }

      // Precipitation
      plot-clean(size: graph-size, y-min: 0, y-max: 120, {
        let precipitation-style = (
          stroke: blue.lighten(50%),
          fill: blue.transparentize(85%),
          // fill: hatching(),
        )

        plot.add(
          line: "hvh",
          hypograph: true,
          style: precipitation-style,
          timestamps.map(t =>
            (parse-date(t).hour(), data.hourly.at(t).precipitation_probability)
          )
        )

      })

      // Temperature
      plot-clean(size: graph-size, x-ticks: ticks, y-min: min-temp - 1, y-max: max-temp + 1,
        name: "temp", {
        let temperature-style = (
          stroke: orange.mix(yellow).lighten(50%),
          fill: yellow.transparentize(75%),
        )

        plot.add(
          line: "spline",
          style: temperature-style,
          timestamps.map(t => (parse-date(t).hour(), data.hourly.at(t).temperature))
        )

        for t in timestamps {
          plot.add-anchor(t, (parse-date(t).hour(), data.hourly.at(t).temperature))
        }
      })

      for t in tick-timestamps {
        draw.content((rel: (0, 0.02), to: "temp." + t),
          text(8pt, gray, str(data.hourly.at(t).temperature))
        )
      }

      // Decorative sun, on top
      draw.content("sun.0", weather-icon("clear-sky-day", width: icon-width))
    })
  })
}

#let weather-display(weather, icon: true, graph: true) = {
  set grid.vline(stroke: 0.5pt)
  set grid(column-gutter: 0pt)

  // Iterate over each day, and for each day, generate a card, vertical line,
  // and graph
  if "by_date" not in weather {
    weather = (by_date: (weather.aggregate.timestamp: weather))
  }

  let cards-and-graphs = weather.by_date.pairs().map(((date, data)) => (
    weather-card(
      date: parse-date(date),
      location: data.aggregate.location,
      statement: [
        #capitalize(data.aggregate.statement.wmo.description),
        #data.aggregate.statement.temperature temps
      ],
      icon: if icon {
        weather-icon(data.aggregate.statement.wmo.owm_image_description)
      },
      hi: data.aggregate.temperature_max,
      lo: data.aggregate.temperature_min,
      precipitation-probability: data.aggregate.precipitation_probability * 1%,
      uv-index: if icon {
        calc.min(data.aggregate.uv_index / 8, 1) * 100%
      },
    ),
    // grid.vline(),
    forecast-graph(data)
  ))

  let inset = (((left: 0em, x: 0.5em),) +
    ((x: 0.5em),) * calc.max(cards-and-graphs.len() - 2, 0) +
    ((right: 0em, x: 0.5em),)
  )

  if graph {
    grid(columns: (1fr, 3fr), align: (top, bottom), row-gutter: 2em,
    inset: inset,
      ..cards-and-graphs.flatten(),
    )
  } else {
    // Remove graphs, and the vline from the last card
    let cards = cards-and-graphs.map(r => r.slice(0, -1))
    cards.at(-1) = cards.at(-1).first()

    grid(columns: cards.len(), align: bottom, inset: inset,
      // Remove graphs
      ..cards.flatten()
    )
  }
}
