#import "@preview/cetz:0.2.2": canvas, draw, plot
#import "weather-rendering.typ": weather-display
#import "dates.typ": parse-date
#import "util.typ": *

// Styling
#show heading.where(level: 1): it => {
  it
  v(0.5em, weak: true)
  line(length: 100%, stroke: 0.5pt)
  v(0.5em, weak: true)
}

#set text(8pt)
#set grid(column-gutter: 8pt)

#show: box

// Read data
#let data = json("./data.json")


#{
  set text(16pt)
  [Good morning, Ischa!]
  h(1fr)
  set text(12pt)
  parse-date(data.timestamp).display("[weekday] [month repr:short] [day], [year]")
  // datetime.today().display()
}

#grid(columns: 3)[
  = Email
][
  = Finance
  #for (account, values) in data.balance_sheet.assets.pairs() {
    let account = account.split(":").slice(1)
    stack(dir: ltr)[
      #capitalize(account.first())
      #if account.len() > 1 [
        (#account.slice(1).join(" "))
      ]
    ][#h(1fr)][
      #stack(dir: ttb, ..values, spacing: 4pt)
    ]
  }
][
  = MOTD
]

#grid(columns: (3fr, 1fr))[
  = News
  // #columns(3, {
    // for article in data.news.chunks(6).first() {
      // box[
        // == #article.title
// 
        // #article.summary.split("\n").chunks(2).first().join(" ")
      // ]
      // linebreak()
      // linebreak()
    // }
  // })

  // Pick an news articles to display
  #let article-count = 9
  #let news = data.news.chunks(article-count).first()
  #let news = news.map(article => {
    box[
      == #text(8pt, article.title)
      // == #article.title
      #set par(justify: true)
      #article.summary.split("\n").chunks(1).first().join(" ")
    ]
    linebreak()
    linebreak()
  })

  #let cols = 3
  #grid(columns: cols, ..news.chunks(int(article-count/cols)).map(c =>
  c.join()))
][
  = To-do's
  #v(4cm)

  = Events
]

= Weather
#weather-display(data.weather.values().first().by_date.values().first())

#if data.weather.len() > 1 or data.weather.values().first().by_date.len() > 1 {
  grid(columns: data.weather.len(), ..data.weather.values().map(data => {
    weather-display(data, graph: false, icon: false)
  }))
}
