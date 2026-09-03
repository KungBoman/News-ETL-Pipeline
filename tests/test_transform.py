from datetime import datetime

from tests.test_helpers import make_test_article
from src.transform import deduplicate_articles

from src.transform import (
    clean_article,
    standardize_article,
    enrich_article,
)


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


def test_clean_article_with_missing_description():
    article = {
        "title": "Test",
        "description": None,
        "url": "https://example.com",
    }

    result = clean_article(article)

    assert result["description"] is None


def test_standardize_article():
    article = {
        "published_at": "Wed, 02 Sep 2026 16:29:05 +0200"
    }

    result = standardize_article(article)

    assert isinstance(result["published_at"], datetime)
    assert result["published_at"].year == 2026
    assert result["published_at"].month == 9
    assert result["published_at"].day == 2


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
