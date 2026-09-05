from src.repository.articles import (
    get_article_by_id,
    get_article_stats,
    get_articles,
)


def test_get_articles(db_connection):
    articles = get_articles(
        db_connection,
        limit=10,
        offset=0,
    )

    assert len(articles) == 3
    assert articles[0][1] == "SVT"
    assert articles[0][2] == "Test article 1"


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


def test_get_articles_with_category_filter(db_connection):
    articles = get_articles(
        db_connection,
        limit=10,
        offset=0,
        category="politics",
    )

    assert len(articles) == 2
    assert all(article[9] == "politics" for article in articles)


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


def test_get_article_stats(db_connection):
    stats = get_article_stats(db_connection)

    assert stats["total_articles"] == 3
    assert stats["politics_related"] == 2
    assert stats["articles_by_source"] == {
        "SVT": 2,
        "Aftonbladet": 1,
    }
