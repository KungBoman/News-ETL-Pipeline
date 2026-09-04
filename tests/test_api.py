from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from src.api import app

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
        (
            1,
            "SVT",
            "Test article",
            "Test description",
            "https://example.com/article",
            datetime(2026, 9, 4, 10, 0, tzinfo=timezone.utc),
            None,
            "Nyheter",
            True,
        )
    ]

    mock_connection.return_value = connection

    response = client.get("/articles/get")

    assert response.status_code == 200

    articles = response.json()

    assert len(articles) == 1
    assert articles[0]["id"] == 1
    assert articles[0]["source"] == "SVT"
    assert articles[0]["title"] == "Test article"
