from unittest.mock import MagicMock, patch

import psycopg
import pytest

from src.load import load_article, load_articles, try_create_connection
from tests.helpers import make_test_article


def test_load_article():
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value

    article = make_test_article()

    load_article(connection, article, commit=True)

    cursor.execute.assert_called_once()
    connection.commit.assert_called_once()


def test_load_article_without_commit():
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value

    article = make_test_article()

    load_article(connection, article, commit=False)

    cursor.execute.assert_called_once()
    connection.commit.assert_not_called()


def test_load_article_raises_on_commit_error():
    connection = MagicMock()
    connection.commit.side_effect = Exception("Commit failed")

    article = make_test_article()

    with pytest.raises(Exception, match="Commit failed"):
        load_article(connection, article, commit=True)


def test_load_articles():
    connection = MagicMock()

    articles = [
        make_test_article(),
        make_test_article(),
    ]

    load_articles(connection, articles, commit=True)

    assert connection.cursor.call_count == 2
    connection.commit.assert_called_once()


def test_load_articles_skips_duplicates():
    connection = MagicMock()

    articles = [
        make_test_article(url="https://example.com/1"),
        make_test_article(url="https://example.com/2"),
    ]

    with patch(
        "src.load.load_article",
        side_effect=[True, False],
    ):
        result = load_articles(
            connection,
            articles,
            commit=True,
        )

    assert result == 1
    connection.commit.assert_called_once()


def test_load_articles_rolls_back_on_error():
    connection = MagicMock()

    connection.cursor.return_value.__enter__.return_value.execute.side_effect = (
        Exception("Database error")
    )

    articles = [
        make_test_article(),
    ]

    with pytest.raises(Exception, match="Database error"):
        load_articles(connection, articles, commit=True)

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()


def test_try_create_connection_retries():
    connection = MagicMock()

    with (
        patch(
            "src.load.create_connection",
            side_effect=[
                psycopg.OperationalError("Connection failed"),
                connection,
            ],
        ),
        patch("src.load.time.sleep") as mock_sleep,
    ):
        result = try_create_connection(
            max_attempts=2,
            retry_delay=1,
        )

    assert result is connection
    mock_sleep.assert_called_once_with(1)


def test_try_create_connection_max_attempts():
    with (
        patch(
            "src.load.create_connection",
            side_effect=psycopg.OperationalError("Connection failed"),
        ),
        patch("src.load.time.sleep") as mock_sleep,
        pytest.raises(
            psycopg.OperationalError,
            match="Connection failed",
        ),
    ):
        try_create_connection(
            max_attempts=3,
            retry_delay=1,
        )

    assert mock_sleep.call_count == 2
