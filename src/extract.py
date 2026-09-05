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


def parse_image_url(entry) -> str | None:
    for link in entry.get("links", []):
        if link.get("type", "").startswith("image/"):
            return link.get("href")

    for media in entry.get("media_content", []):
        if media.get("url"):
            return media.get("url")

    return None


def parse_author_info(entry, field: str) -> str | None:
    for author in entry.get("authors", []):
        return author.get(field)

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
                    "published_at": published_at,
                    "text_url": entry.get("link"),
                    "image_url": parse_image_url(entry),
                    "summary": entry.get("summary"),
                    "author_name": parse_author_info(entry, "name"),
                    "author_email": parse_author_info(entry, "email"),
                }
            )

        logger.info(f"Extracted {len(articles)} articles from {source}")

        return articles

    except Exception:
        logger.exception(f"Failed to extract articles from {source}")
        raise
