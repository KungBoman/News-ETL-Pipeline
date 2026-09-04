from unittest.mock import patch

from src.config import RSS_SOURCES
from src.extract import extract_rss


class MockFeed:
    def __init__(self, entries):
        self.entries = entries
        self.bozo = True


def test_extract_rss():
    mock_feed = MockFeed([
        {
            "title": "Test article",
            "description": "Test description",
            "link": "https://example.com",
            "published_parsed": (2026, 9, 2, 16, 29, 5),
            "author": "Test Author",
            "category": "News",
        }
    ])

    with patch("src.extract.feedparser.parse", return_value=mock_feed):
        result = extract_rss("https://example.com/rss", "Test Source")

    assert len(result) == 1
    assert result[0]["source"] == "Test Source"
    assert result[0]["title"] == "Test article"
    assert result[0]["description"] == "Test description"
    assert result[0]["url"] == "https://example.com"


def test_all_rss_sources():
    for source in RSS_SOURCES:
        articles = extract_rss(
            source["url"],
            source["name"],
        )

        assert len(articles) > 0
        assert all(
            article["source"] == source["name"]
            for article in articles
        )
