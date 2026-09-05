from src.validate import validate_article, validate_articles
from tests.helpers import make_test_article


def test_valid_article():
    article = make_test_article()

    assert validate_article(article) is True


def test_article_without_title_is_invalid():
    article = make_test_article()
    article["title"] = None

    assert validate_article(article) is False


def test_article_without_text_url_is_invalid():
    article = make_test_article()
    article["text_url"] = None

    assert validate_article(article) is False


def test_article_without_published_at_is_invalid():
    article = make_test_article()
    article["published_at"] = None

    assert validate_article(article) is False


def test_validate_articles_returns_valid_articles():
    valid_article = make_test_article(text_url="https://example.com/valid")

    invalid_article = make_test_article(text_url="https://example.com/invalid")
    invalid_article["title"] = None

    result = validate_articles(
        [
            valid_article,
            invalid_article,
        ]
    )

    assert result == [valid_article]


def test_validate_articles_returns_all_valid_articles():
    articles = [
        make_test_article(text_url="https://example.com/1"),
        make_test_article(text_url="https://example.com/2"),
    ]

    result = validate_articles(articles)

    assert result == articles
