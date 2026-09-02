import feedparser

from src.models import Article


SVT_RSS_URL = "http://www.svt.se/nyheter/sverige/rss.xml"


def extract_rss(url: str, source: str) -> list[Article]:
    feed = feedparser.parse(url)

    articles: list[Article] = []

    for entry in feed.entries:
        articles.append({
            "source": source,
            "title": entry.get("title"),
            "description": entry.get("description"),
            "url": entry.get("link"),
            "published_at": entry.get("published"),
            "author": entry.get("author"),
            "category": entry.get("category"),
            "is_politics_related": False,
        })

    return articles
