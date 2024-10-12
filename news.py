from util import *
import feedparser

@dataclass
class Article:
    title: str
    summary: str
    url: str
    timestamp: datetime

    def __str__(self):
        return f"{self.title}\n{self.timestamp}\n" + self.summary

    def __post_init__(self):
        self.summary = parse_html(self.summary)


def fetch_rss_articles(url: str) -> List[Article]:
    data = feedparser.parse(url)

    articles = []

    for entry in data.entries:
        articles.append(Article(
            title=entry["title"],
            summary=entry["summary"],
            url=entry["link"],
            timestamp=datetime(*entry["published_parsed"][:5]),
        ))

    return articles

fetch_articles = fetch_rss_articles
