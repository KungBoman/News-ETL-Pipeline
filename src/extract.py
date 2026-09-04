from datetime import datetime, timezone

import feedparser

from src.logger import get_logger
from src.models import Article

SVT_RSS_URL = "http://www.svt.se/nyheter/sverige/rss.xml"

logger = get_logger(__name__)


def parse_published_at(entry) -> datetime | None:
    published_at = entry.get("published_parsed")

    if not published_at:
        return None

    return datetime(
        *published_at[:6],
        tzinfo=timezone.utc,
    )


def extract_rss(url: str, source: str) -> list[Article]:
    logger.info(f"Starting extraction from {source}...")

    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            logger.warning(f"RSS feed for {source} may be malformed")

        articles: list[Article] = []

        for entry in feed.entries:

            articles.append({
                "source": source,
                "title": entry.get("title"),
                "description": entry.get("description"),
                "url": entry.get("link"),
                "published_at": parse_published_at(entry),
                "author": entry.get("author"),
                "category": entry.get("category"),
            })

        logger.info(f"Extracted {len(articles)} articles from {source}")

        return articles

    except Exception:
        logger.exception(f"Failed to extract articles from {source}")
        raise
