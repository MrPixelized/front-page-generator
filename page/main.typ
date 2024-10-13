#import "@preview/cetz:0.2.2": canvas, draw, plot
#import "weather-rendering.typ": weather-display
#import "dates.typ": parse-date
#import "util.typ": *

#let currency-sign(name) = (
  "EUR": sym.euro,
  "USD": sym.dollar,
).at(name)

#let censor(c) = context box(rect(
  height: measure(c).height, width: measure(c).width,
  inset: 0em, outset: (bottom: 1pt), fill: black.lighten(20%)
))
// #let censor(c) = c

#let base-finance-summary(data) = {
  // Make sure total is at the end
  if "total" in data {
    data.insert("total", data.remove("total"))
  }

  for (account, values) in data.pairs() {
    if account == "total" {
      account = strong[#h(0.5em)#sym.arrow.r.curve]
      values = values.map(strong)
    } else {
      account = account.split(":").slice(1)
      account = [
        #capitalize(account.first())
        #if account.len() > 1 [
          (#(censor(account.slice(1).join(" "))))
        ]
      ]
    }

    stack(dir: ltr)[
      #account
    ][#h(1fr)][
      #stack(dir: ttb, ..values, spacing: 4pt)
    ]

    v(0.65em, weak: true)
  }
}

#let currency-amount(a) = a.map(v => censor[
  #currency-sign(v.split().last())#v.split().first()
])

#let budget-summary(data) = {
  for (account, values) in data.pairs() {
    values = values.used.zip(values.total).map(currency-amount).map(v =>
    v.join("/"))
    data.insert(account, values)
  }
  let _ = data.remove("total")
  base-finance-summary(data)
}

#let account-summary(data) = {
  for (account, values) in data.pairs() {
    data.insert(account, currency-amount(values.first()))
  }
  base-finance-summary(data)
}

// Styling
#show heading.where(level: 1): it => {
  it
  v(0.5em, weak: true)
  line(length: 100%, stroke: 0.5pt)
  v(0.5em, weak: true)
}

#set text(8pt)
#set par(leading: 0.5em, justify: true)
#set grid(column-gutter: 8pt, row-gutter: 16pt)
#set columns(gutter: 8pt)

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

#let calendar = [
  = Events today

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

#let news = [
  = News
  #let article-count = 9
  #let cols = 3
  #let news = data.news.chunks(article-count).first()
  #let news = news.map(article => {
      heading(level: 2, par(leading: 0.33em, justify: false, text(8pt, article.title)))
      article.summary.split("\n").chunks(1).first().join(" ")
  })

  #block(clip: true, inset: (bottom: 0.2em),
    // columns(cols, news.join({v(1em);v(1fr, weak: true)}))

    grid(columns: cols,
      ..news.chunks(int(article-count/cols)).map(c => c.join(v(1em, weak: true)))
    )
  )
]

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

#title

#grid(columns: 1fr, rows: (auto, 1fr, auto),
  weather,
  grid(columns: (1fr, 4cm),
    news,
    grid(columns: 1,
      calendar,
      todo,
      finance,
    ),
  ),
  grid(columns: 3,
    motd,
    email,
  ),
)
