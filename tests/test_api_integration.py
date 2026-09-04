from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_get_articles_integration(db_connection):
    response = client.get("/articles/")

    assert response.status_code == 200

    articles = response.json()

    assert len(articles) == 3
    assert articles[0]["source"] == "SVT"
    assert articles[0]["title"] == "Test article 1"


def test_get_articles_with_pagination_integration(db_connection):
    response = client.get("/articles/?limit=2&offset=0")

    assert response.status_code == 200

    articles = response.json()

    assert len(articles) == 2


def test_get_articles_with_offset_integration(db_connection):
    response = client.get("/articles/?limit=2&offset=2")

    assert response.status_code == 200

    articles = response.json()

    assert len(articles) == 1


def test_get_articles_with_source_filter_integration(db_connection):
    response = client.get("/articles/?source=SVT")

    assert response.status_code == 200

    articles = response.json()

    assert len(articles) == 2
    assert all(article["source"] == "SVT" for article in articles)


def test_get_articles_with_politics_filter_integration(db_connection):
    response = client.get("/articles/?is_politics_related=true")

    assert response.status_code == 200

    articles = response.json()

    assert len(articles) == 2
    assert all(article["is_politics_related"] is True for article in articles)
