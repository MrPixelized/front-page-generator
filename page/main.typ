#import "@preview/cetz:0.2.2": canvas, draw, plot
#import "weather-rendering.typ": weather-display
#import "dates.typ": parse-date

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
][
  = MOTD
]

#v(1fr)

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
#let here = data.weather.keys().first()
#let now = data.weather.at(here).by_date.keys().first()
// #let weather-today-here = data.weather.at(here).by_date.remove(now)

#weather-display(data.weather.at(here), graph: true)
// #if data.weather.at(here).weather.aggregate.len() > 0 {
  // for data in data.weather.values() {
    // weather-display(data.weather, location: data.location, graph: false, icon: false)
  // }
// }
