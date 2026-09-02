from src.validate import validate_article


def make_test_article() -> dict:
    return {
        "source": "SVT",
        "title": "Test article",
        "url": "https://example.com",
        "published_at": "2026-09-02",
    }


def test_valid_article():
    article = make_test_article()

    assert validate_article(article) is True


def test_article_without_title_is_invalid():
    article = make_test_article()
    article["title"] = None

    assert validate_article(article) is False


def test_article_without_url_is_invalid():
    article = make_test_article()
    article["url"] = None

    assert validate_article(article) is False


def test_article_without_published_at_is_invalid():
    article = make_test_article()
    article["published_at"] = None

    assert validate_article(article) is False
