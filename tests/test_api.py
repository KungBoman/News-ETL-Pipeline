import pytest

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from src.api import app
from tests.helpers import make_article_row

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "Swedish News ETL API"


@patch("src.routers.articles.try_create_connection")
def test_get_articles(mock_connection):
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value

    cursor.fetchall.return_value = [
        make_article_row()
    ]

    mock_connection.return_value = connection

    response = client.get("/articles/")

    assert response.status_code == 200

    articles = response.json()

    assert len(articles) == 1
    assert articles[0]["id"] == 1
    assert articles[0]["source"] == "SVT"
    assert articles[0]["title"] == "Test article"


@patch("src.routers.articles.try_create_connection")
@patch("src.routers.articles.get_articles")
def test_get_articles_with_pagination(mock_get_articles, mock_connection):
    connection = MagicMock()
    mock_connection.return_value = connection

    mock_get_articles.return_value = []

    response = client.get(
        "/articles/?limit=10&offset=20"
    )

    assert response.status_code == 200

    mock_get_articles.assert_called_once_with(
        connection,
        limit=10,
        offset=20,
        source=None,
        is_politics_related=None,
    )


@patch("src.routers.articles.try_create_connection")
@patch("src.routers.articles.get_articles")
def test_get_articles_with_filter(mock_get_articles, mock_connection):
    connection = MagicMock()
    mock_connection.return_value = connection

    mock_get_articles.return_value = []

    response = client.get(
        "/articles/?source=SVT&is_politics_related=true"
    )

    assert response.status_code == 200

    mock_get_articles.assert_called_once_with(
        connection,
        limit=20,
        offset=0,
        source="SVT",
        is_politics_related=True,
    )


@patch("src.routers.articles.try_create_connection")
@patch("src.routers.articles.get_article_by_id")
def test_get_article(mock_get_article, mock_connection):
    connection = MagicMock()
    mock_connection.return_value = connection

    mock_get_article.return_value = make_article_row()

    response = client.get("/articles/1")

    assert response.status_code == 200

    article = response.json()

    assert article["id"] == 1
    assert article["source"] == "SVT"
    assert article["title"] == "Test article"


@patch("src.routers.articles.try_create_connection")
@patch("src.routers.articles.get_article_by_id")
def test_get_article_not_found(mock_get_article, mock_connection):
    connection = MagicMock()
    mock_connection.return_value = connection

    mock_get_article.return_value = None

    response = client.get("/articles/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Article not found"
    }


@patch("src.routers.health.try_create_connection")
def test_health(mock_connection):
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value

    mock_connection.return_value = connection

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "ok",
    }

    cursor.execute.assert_called_once_with("SELECT 1")
    connection.close.assert_called_once()


@patch("src.routers.health.try_create_connection")
def test_health_closes_connection_on_error(mock_connection):
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value

    cursor.execute.side_effect = Exception("Database error")
    mock_connection.return_value = connection

    with pytest.raises(Exception, match="Database error"):
        client.get("/health")

    connection.close.assert_called_once()
