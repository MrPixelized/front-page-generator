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
