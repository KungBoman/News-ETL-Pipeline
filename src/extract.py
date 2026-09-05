from datetime import datetime, timezone

import feedparser  # type: ignore[import-untyped]

from src.logger import get_logger
from src.models import Article

logger = get_logger(__name__)


def parse_published_at(entry) -> datetime | None:
    published_at = entry.get("published_parsed")

    if published_at:
        y, mo, d, h, mi, s = published_at[:6]
        return datetime(y, mo, d, h, mi, s, tzinfo=timezone.utc)

    return None


def extract_rss(url: str, source: str) -> list[Article]:
    logger.info(f"Starting extraction from {source}...")

    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            logger.warning(f"RSS feed for {source} may be malformed")

        articles: list[Article] = []

        for entry in feed.entries:
            published_at = parse_published_at(entry)

            if published_at is None:
                logger.warning(f"Skipping article from {source}: missing published_at")
                continue

            articles.append(
                {
                    "source": source,
                    "title": entry.get("title"),
                    "summary": entry.get("summary"),
                    "url": entry.get("link"),
                    "published_at": published_at,
                    "author": entry.get("author"),
                    "category": entry.get("category"),
                }
            )

        logger.info(f"Extracted {len(articles)} articles from {source}")

        return articles

    except Exception:
        logger.exception(f"Failed to extract articles from {source}")
        raise
