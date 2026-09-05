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
        "summary": "  Test summary  ",
        "text_url": " https://example.com ",
        "author_name": None,
    }

    result = clean_article(article)

    assert result["title"] == "Test article"
    assert result["summary"] == "Test summary"
    assert result["text_url"] == "https://example.com"
    assert result["author_name"] is None


def test_clean_article_handles_optional_fields():
    article = make_test_article()
    article["author_name"] = "  Test Author  "
    article["author_email"] = "  Test Email  "

    result = clean_article(article)

    assert result["author_name"] == "Test Author"
    assert result["author_email"] == "Test Email"


def test_clean_article_handles_missing_optional_fields():
    article = make_test_article()
    article["summary"] = None
    article["author_name"] = None
    article["author_email"] = None

    result = clean_article(article)

    assert result["summary"] is None
    assert result["author_name"] is None
    assert result["author_email"] is None


def test_standardize_article():
    article = make_test_article()

    result = standardize_article(article)

    assert result["published_at"] == article["published_at"]


def test_enrich_article():
    article = make_test_article(
        title="Regeringen presenterar nytt förslag",
    )
    article["summary"] = "Statsministern kommenterar förslaget"

    result = enrich_article(article)

    assert result["is_politics_related"] is True


def test_enrich_article_not_politics_related():
    article = make_test_article(
        title="Ny AI-modell lanserad",
    )
    article["summary"] = "Företaget presenterar sin nya modell"

    result = enrich_article(article)

    assert result["is_politics_related"] is False


def test_deduplicate_articles():
    articles = [
        make_test_article(text_url="https://example.com/1"),
        make_test_article(text_url="https://example.com/1"),
        make_test_article(text_url="https://example.com/2"),
    ]

    result = deduplicate_articles(articles)

    assert len(result) == 2
    assert result[0]["text_url"] == "https://example.com/1"
    assert result[1]["text_url"] == "https://example.com/2"


def test_transform_articles():
    articles = [
        make_test_article(
            title="  Regeringen presenterar förslag  ",
            text_url=" https://example.com/1 ",
        ),
        make_test_article(
            title="Duplicate article",
            text_url=" https://example.com/1 ",
        ),
    ]

    result = transform_articles(articles)

    assert len(result) == 1
    assert result[0]["title"] == "Regeringen presenterar förslag"
    assert result[0]["text_url"] == "https://example.com/1"
    assert result[0]["is_politics_related"] is True
