#import "@preview/cetz:0.2.2": canvas, draw, plot
#import "weather-rendering.typ": weather-display
#import "dates.typ": parse-date
#import "util.typ": *

#let currency-sign(name) = (
  "EUR": sym.euro,
  "USD": sym.dollar,
).at(name)

#let account-summary(data) = for (account, values) in data.pairs() {
  values = values.map(v => [
    #currency-sign(v.split().last())#v.split().first()
  ])

  if account == "total" {
    account = strong[#h(0.5em)#sym.arrow.r.curve]
    values = values.map(strong)
  } else {
    account = account.split(":").slice(1)
    account = [
      #capitalize(account.first())
      #if account.len() > 1 [
        (#(account.slice(1).join(" ")))
      ]
    ]
  }

  stack(dir: ltr)[
    #account
  ][#h(1fr)][
    #stack(dir: ttb, ..values, spacing: 4pt)
  ]

  v(0.5em, weak: true)
}

// Styling
#show heading.where(level: 1): it => {
  it
  v(0.5em, weak: true)
  line(length: 100%, stroke: 0.5pt)
  v(0.5em, weak: true)
}

#set text(8pt)
#set grid(column-gutter: 8pt, row-gutter: 16pt)

// Read data
#let data = json("./data.json")

// Title
#{
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
  = Events
]

#let motd = [
  = MOTD

  #lorem(40)
]

#let news = [
  = News
  #let article-count = 12
  #let news = data.news.chunks(article-count).first()
  #let news = news.map(article => {
    box[
      #set par(justify: true)
      == #text(8pt, article.title)
      #article.summary.split("\n").chunks(1).first().join(" ")
    ]
  })

  #let cols = 3
  #grid(columns: cols, ..news.chunks(int(article-count/cols)).map(c =>
  c.join(v(1em, weak: true))))
]

#let finance = [
  = Finance
  == Assets
  #account-summary(data.balance_sheet.assets)

  #v(0.5em)
  == Liabilities
  #account-summary(data.balance_sheet.liabilities)

  #v(0.5em)
  == Net
  #account-summary(data.balance_sheet.net)
]

#let todo = [
  = To-do's
  #v(4cm)
]

#let weather = [
  = Weather
  #weather-display(data.weather.values().first().by_date.values().first())

  #if data.weather.len() > 1 or data.weather.values().first().by_date.len() > 1 {
    grid(columns: data.weather.len(), ..data.weather.values().map(data => {
      weather-display(data, graph: false, icon: false)
    }))
  }
]

// #show: box

#grid(columns: 1fr,
  weather,
  grid(columns: (1fr, 4cm),
    news,
    grid(columns: 1,
      finance,
      todo
    ),
  ),
  grid(columns: 3,
    motd,
    email,
    calendar
  ),
)
