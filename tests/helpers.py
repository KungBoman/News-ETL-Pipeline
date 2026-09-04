from datetime import datetime, timezone

from src.models import Article


def make_test_article(
    source="SVT",
    title="Test article",
    url="https://example.com",
    published_at=datetime(2026, 9, 2, 10, 0, tzinfo=timezone.utc),
) -> Article:
    return {
        "source": source,
        "title": title,
        "description": "Test description",
        "url": url,
        "published_at": published_at,
        "author": None,
        "category": None,
        "is_politics_related": False
    }


def make_article_row(
    article_id: int = 1,
    source: str = "SVT",
    title: str = "Test article",
    url: str = "https://example.com",
    published_at=datetime(2026, 9, 2, 10, 0, tzinfo=timezone.utc),
):
    return (
        article_id,
        source,
        title,
        "Test description",
        url,
        published_at,
        None,
        None,
        False,
    )
