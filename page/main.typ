#import "@preview/cetz:0.2.2": canvas, draw, plot
#import "weather.typ": weather-display
#import "finance.typ": budget-summary, account-summary
#import "dates.typ": parse-date
#import "util.typ": *

// Styling
#show heading.where(level: 1): it => {
  it
  v(0.5em, weak: true)
  line(length: 100%, stroke: 0.5pt)
  v(0.5em, weak: true)
}
#show heading.where(level: 2): set par(justify: false)
#show heading.where(level: 2): it => {
  it
  v(0.5em, weak: true)
}

#set page(margin: 2cm)
#set text(8pt)
#show heading.where(level: 2): set par(leading: 0.33em)
#set par(leading: 0.5em, justify: true)
#set grid(column-gutter: 8pt, row-gutter: 16pt)
#set columns(gutter: 8pt)
#set quote(block: true)

// Read data
#let data = json("./data.json")

// Title
#let title = {
  set text(16pt)
  [Good morning, Ischa!]
  h(1fr)
  set text(12pt)
  parse-date(data.timestamp).display("[weekday] [month repr:short] [day], [year]")
}


#let email = [
  = Email
]

#let transit = [
  = Transit
]

#let astronomy = [
  = Astronomy
]

#let calendar = [
  = Events today

  #if data.events.len() == 0 [
    I guess today's just chillin'.
  ]

  #set par(justify: false)
  #let colors = (yellow, blue, orange, green, red, purple)
  #for event in data.events {
    let start = parse-date(event.start_time)
    let end = parse-date(event.end_time)
    let c = colors.at(calc.rem(start.hour(), colors.len()))

    rect(radius: 0.5em, stroke: 0pt, fill: c.lighten(80%), width: 100%)[
      #event.title
      #h(1fr)
      // #sym.dot.c
      #if start == end [
        #start.display("[hour]:[minute]")
      ] else [
        #start.display("[hour]:[minute]") -- #end.display("[hour]:[minute]")
      ]
    ]
    v(0.5em, weak: true)
  }
]

#let motd = [
  = MOTD

  #lorem(50)
]

#let quote = [
  #set par(justify: false)
  // = QOTD
  // #v(8pt, weak: true)
  #quote(attribution: data.quote.author, data.quote.text)
]

#let news(articles: none, cols: 3) = context layout(size => [
  #let max = if articles != none { articles } else { data.news.len() }
  #let min = if articles != none { articles } else { cols }

  #let news-columns(a) = {
    let news = data.news.chunks(a).first()
    news = news.map(article => [
      #show heading.where(level: 2): set text(text.size)
      // #strong(article.title)
      // #h(0.65em)
      == #article.title
      #shorten-text(article.summary)
    ])

    block(width: size.width,
      grid(columns: cols,
        ..divide-in-chunks(news, cols).map(col => col.join({
          // strong(sym.dot.op)
          v(1em)
          v(1fr, weak: true)
        }))
      )
    )
  }

  = News
  #for articles in range(min, max, step: 1) {
    if measure(news-columns(articles)).height > size.height - 8pt {
      news-columns(articles - 1)
      break
    }
  }
])

#let finance = [
  = Finance
  #if data.finance.budget_sheet.budgets.len() > 1 [
    == Budgets
    #budget-summary(data.finance.budget_sheet.budgets)
    #v(0.5em)
  ]

  == Assets
  #account-summary(data.finance.balance_sheet.assets)

  #if data.finance.balance_sheet.liabilities.len() > 1 [
    #v(0.5em)
    == Liabilities
    #account-summary(data.finance.balance_sheet.liabilities)

    #v(0.5em)
    == Net
    #account-summary(data.finance.balance_sheet.net)
  ]
]

#let todo = [
  = To-dos
  #for event in data.todo {
    let due = parse-date(event.due)

    rect(radius: 0.5em, stroke: 0pt, fill: blue.lighten(80%), width: 100%)[
      #if due != none [
        #due.display("[hour]:[minute]")
      ]
      #event.title
      #h(1fr)
      #box(rect(radius: 1pt, inset: 2.5pt, outset: 0em, stroke: 0.5pt, fill:
      white)[]) 
    ]
    v(0.5em, weak: true)
  }
]

#let weather = [
  = Weather
  #weather-display(data.weather.values().first().by_date.values().first())

  #if data.weather.len() > 1 or data.weather.values().first().by_date.len() > 1 {
    grid(columns: data.weather.len(),
      ..data.weather.values().map(
        weather-display.with(graph: false, icon: false)
      )
    )
  }
]


#show: box
// #title

#grid(columns: 1fr, rows: (auto, 1fr, auto),
  weather,
  grid(columns: (3fr, 1fr),
    news(),
    grid(columns: 1, row-gutter: (16pt, 16pt, 1fr),
      calendar,
      todo,
      finance,
      quote,
    ),
  ),
  // grid(columns: (2fr, 3fr, 2fr),
    // motd,
    // astronomy,
    // transit,
  // ),
)
