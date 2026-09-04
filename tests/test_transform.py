from datetime import datetime, timezone

from src.transform import (
    clean_article,
    deduplicate_articles,
    enrich_article,
    standardize_article,
    transform_articles,
)
from tests.helpers import make_test_article


def test_clean_article():
    article = {
        "title": "  Test article  ",
        "description": "  Some description  ",
        "url": " https://example.com ",
        "author": None,
        "category": "",
    }

    result = clean_article(article)

    assert result["title"] == "Test article"
    assert result["description"] == "Some description"
    assert result["url"] == "https://example.com"
    assert result["author"] is None
    assert result["category"] is None


def test_clean_article_handles_optional_fields():
    article = make_test_article()
    article["author"] = "  Test Author  "
    article["category"] = "  Great category  "

    result = clean_article(article)

    assert result["author"] == "Test Author"
    assert result["category"] == "Great category"


def test_clean_article_handles_missing_optional_fields():
    article = make_test_article()
    article["description"] = None
    article["author"] = None
    article["category"] = None

    result = clean_article(article)

    assert result["description"] is None
    assert result["author"] is None
    assert result["category"] is None


def test_standardize_article():
    article = make_test_article(
        published_at=datetime(
            2026, 9, 2, 16, 29, 5,
            tzinfo=timezone.utc,
        )
    )

    result = standardize_article(article)

    assert result["published_at"] == article["published_at"]


def test_enrich_article():
    article = {
        "title": "Regeringen presenterar nytt förslag",
        "description": "Statsministern kommenterar förslaget."
    }

    result = enrich_article(article)

    assert result["is_politics_related"] is True


def test_enrich_article_not_politics_related():
    article = {
        "title": "Ny AI-modell lanserad",
        "description": "Företaget presenterar sin nya modell."
    }

    result = enrich_article(article)

    assert result["is_politics_related"] is False


def test_deduplicate_articles():
    articles = [
        make_test_article(url="https://example.com/1"),
        make_test_article(url="https://example.com/1"),
        make_test_article(url="https://example.com/2"),
    ]

    result = deduplicate_articles(articles)

    assert len(result) == 2
    assert result[0]["url"] == "https://example.com/1"
    assert result[1]["url"] == "https://example.com/2"


def test_transform_articles():
    articles = [
        make_test_article(
            title="  Regeringen presenterar förslag  ",
            url=" https://example.com/1 ",
        ),
        make_test_article(
            title="Duplicate article",
            url=" https://example.com/1 ",
        ),
    ]

    result = transform_articles(articles)

    assert len(result) == 1
    assert result[0]["title"] == "Regeringen presenterar förslag"
    assert result[0]["url"] == "https://example.com/1"
    assert result[0]["is_politics_related"] is True
