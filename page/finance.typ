#import "dates.typ": parse-date
#import "util.typ": *

#let censor(c) = context box(rect(
  height: measure(c).height, width: measure(c).width,
  inset: 0em, outset: (bottom: 1pt), fill: black.lighten(20%)
))
#let censor(c) = c

#let currency-sign(name) = (
  "EUR": sym.euro,
  "USD": sym.dollar,
).at(name)

#let currency-amount(a) = a.map(v => censor[
  #currency-sign(v.split().last())#v.split().first()
])

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
