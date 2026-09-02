import feedparser

SVT_RSS_URL = "http://www.svt.se/nyheter/sverige/rss.xml"


def extract_rss(url: str, source: str) -> list[dict]:
    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries:
        articles.append({
            "source": source,
            "title": entry.get("title"),
            "description": entry.get("description"),
            "url": entry.get("link"),
            "published_at": entry.get("published"),
            "author": entry.get("author"),
            "category": entry.get("category"),
        })

    return articles
