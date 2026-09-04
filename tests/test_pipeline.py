from unittest.mock import MagicMock, patch

from src.pipeline import run_pipeline
from tests.helpers import make_test_article


def test_run_pipeline():
    articles = [
        make_test_article(url="https://example.com/1"),
        make_test_article(url="https://example.com/2"),
    ]

    mock_connection = MagicMock()

    with (
        patch("src.pipeline.extract_rss", return_value=articles) as mock_extract,
        patch(
            "src.pipeline.transform_articles",
            return_value=articles,
        ) as mock_transform,
        patch(
            "src.pipeline.validate_articles",
            return_value=articles,
        ) as mock_validate,
        patch(
            "src.pipeline.try_create_connection",
            return_value=mock_connection,
        ),
        patch(
            "src.pipeline.load_articles",
            return_value=2,
        ) as mock_load,
    ):
        stats = run_pipeline()

        assert stats == {
            "extracted": 8,
            "transformed": 2,
            "valid": 2,
            "loaded": 2,
        }

        assert mock_extract.call_count == 4
        mock_transform.assert_called_once()
        mock_validate.assert_called_once()
        mock_load.assert_called_once()

        mock_connection.close.assert_called_once()


def test_run_pipeline_continues_when_source_extraction_fails():
    connection = MagicMock()

    article = make_test_article()

    with (
        patch(
            "src.pipeline.extract_rss",
            side_effect=[
                Exception("SVT unavailable"),
                [article],
                [article],
                [article],
            ],
        ) as mock_extract,
        patch(
            "src.pipeline.transform_articles",
            return_value=[article],
        ) as mock_transform,
        patch(
            "src.pipeline.validate_articles",
            return_value=[article],
        ) as mock_validate,
        patch(
            "src.pipeline.try_create_connection",
            return_value=connection,
        ),
        patch(
            "src.pipeline.load_articles",
            return_value=1,
        ) as mock_load,
    ):
        stats = run_pipeline()

        assert stats == {
            "extracted": 3,
            "transformed": 1,
            "valid": 1,
            "loaded": 1,
        }

        assert mock_extract.call_count == 4
        mock_transform.assert_called_once()
        mock_validate.assert_called_once()
        mock_load.assert_called_once()
        connection.close.assert_called_once()
