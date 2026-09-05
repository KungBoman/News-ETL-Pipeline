from unittest.mock import patch

import pytest

from src.config import RSS_SOURCES
from src.extract import extract_rss


class MockFeed:
    def __init__(self, entries):
        self.entries = entries
        self.bozo = True


def test_extract_rss():
    mock_feed = MockFeed(
        [
            {
                "title": "Test article",
                "summary": "Test summary",
                "link": "https://example.com",
                "links": [
                    {
                        "type": "image/jpeg",
                        "href": "https://example.com/image.jpg",
                    }
                ],
                "published_parsed": (2026, 9, 2, 16, 29, 5),
                "authors": [
                    {
                        "name": "Test Author",
                        "email": "test@example.com",
                    }
                ],
            }
        ]
    )

    with patch("src.extract.feedparser.parse", return_value=mock_feed):
        result = extract_rss("https://example.com/rss", "Test Source")

    assert len(result) == 1
    assert result[0]["source"] == "Test Source"
    assert result[0]["title"] == "Test article"
    assert result[0]["summary"] == "Test summary"
    assert result[0]["text_url"] == "https://example.com"
    assert result[0]["image_url"] == "https://example.com/image.jpg"
    assert result[0]["author_name"] == "Test Author"
    assert result[0]["author_email"] == "test@example.com"


def test_extract_rss_without_published_at():
    with (
        patch("src.extract.feedparser.parse") as mock_parse,
        patch("src.extract.parse_published_at", return_value=None),
    ):
        mock_parse.return_value.entries = [{"title": "Test article"}]

        result = extract_rss("https://example.com/rss", "Test Source")

    assert result == []


def test_extract_rss_feedparser_error():
    with (
        patch(
            "src.extract.feedparser.parse",
            side_effect=Exception("RSS error"),
        ),
        pytest.raises(Exception, match="RSS error"),
    ):
        extract_rss("https://example.com/rss", "Test Source")


def test_all_rss_sources():
    for source in RSS_SOURCES:
        articles = extract_rss(
            source["url"],
            source["name"],
        )

        assert len(articles) > 0
        assert all(article["source"] == source["name"] for article in articles)
