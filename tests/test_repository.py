from src.repository.articles import (
    get_article_by_id,
    get_articles,
)
from src.repository.articles import get_articles


def test_get_articles(db_connection):
    articles = get_articles(
        db_connection,
        limit=10,
        offset=0,
    )

    assert len(articles) == 3
    assert articles[0]["source"] == "SVT"
    assert articles[0]["title"] == "Test article"


def test_get_articles_with_pagination(db_connection):
    articles = get_articles(
        db_connection,
        limit=1,
        offset=0,
    )

    assert len(articles) == 1


def test_get_articles_with_source_filter(db_connection):
    articles = get_articles(
        db_connection,
        limit=10,
        offset=0,
        source="SVT",
    )

    assert len(articles) == 2
    assert all(article[1] == "SVT" for article in articles)


def test_get_articles_with_politics_filter(db_connection):
    articles = get_articles(
        db_connection,
        limit=10,
        offset=0,
        is_politics_related=True,
    )

    assert len(articles) == 2
    assert all(article[8] is True for article in articles)


def test_get_article_by_id(db_connection):
    article = get_article_by_id(
        db_connection,
        article_id=1,
    )

    assert article is not None
    assert article[0] == 1
    assert article[1] == "SVT"
    assert article[2] == "Test article 1"


def test_get_article_by_id_not_found(db_connection):
    article = get_article_by_id(
        db_connection,
        article_id=999,
    )

    assert article is None
