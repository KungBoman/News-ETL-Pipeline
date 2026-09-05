from datetime import datetime, timezone

from src.models import Article


def make_test_article(
    source="SVT",
    title="Test article",
    published_at=datetime(2026, 9, 2, 10, 0, tzinfo=timezone.utc),
    text_url="https://example.com",
) -> Article:
    return {
        "source": source,
        "title": title,
        "published_at": published_at,
        "text_url": text_url,
        "image_url": None,
        "summary": None,
        "author_name": None,
        "author_email": None,
    }


def make_article_row(
    article_id: int = 1,
    source: str = "SVT",
    title: str = "Test article",
    published_at=datetime(2026, 9, 2, 10, 0, tzinfo=timezone.utc),
    text_url: str = "https://example.com",
):
    return (
        article_id,
        source,
        title,
        published_at,
        text_url,
        None,  # image_url
        None,  # summary
        None,  # author_name
        None,  # author_email
        None,  # category
        False,  # is_politics_related
    )
