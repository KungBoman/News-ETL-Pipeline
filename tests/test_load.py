from unittest.mock import MagicMock

import pytest

from src.load import load_article, load_articles
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
