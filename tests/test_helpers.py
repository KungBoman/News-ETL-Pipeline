from datetime import datetime

from src.models import Article


def make_test_article(
    source="SVT",
    title="Test article",
    url="https://example.com",
    published_at=datetime(2026, 9, 2),
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
