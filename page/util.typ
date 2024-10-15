#let capitalize(s) = upper(s.slice(0, 1)) + s.slice(1)

#let divide-in-chunks(arr, n) = {
  let chunk-size = int(arr.len() / n)

  if chunk-size == 0 {
    chunk-size = 1
  }

  let chunks = arr.chunks(chunk-size)

  if chunks.len() == n {
    return chunks
  }

  for (i, e) in chunks.last().enumerate() {
    chunks.at(i).push(e)
  }

  return chunks.slice(0, -1)
}

#let shorten-text(t, len: 240) = {
  if t.split("-").first().ends-with("(Reuters) ") {
    t = t.split("-").slice(1).join("-")
  }

  let shortened = t.split("\n").chunks(1).first().join(" ")

  // return shortened

  if shortened.len() > len {
    let sp = shortened.split(". ")
    if sp.len() > 1 {
      shortened = sp.chunks(1).first().join(". ") + "."
    }
  }

  shortened.trim()
}

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
    values = values.used.zip(values.total).map(currency-amount)

    if account == "total" {
      values = values.map(array.first)
    } else {
      values = values.map(v => v.join("/"))
    }
    data.insert(account, values)
  }

  base-finance-summary(data)
}

#let account-summary(data) = {
  for (account, values) in data.pairs() {
    data.insert(account, currency-amount(values.first()))
  }
  base-finance-summary(data)
}
