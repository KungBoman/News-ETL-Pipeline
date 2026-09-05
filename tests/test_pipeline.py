from unittest.mock import MagicMock, patch

import pytest

from src.config import RSS_SOURCES
from src.pipeline import run_pipeline
from tests.helpers import make_test_article


def test_run_pipeline():
    articles = [
        make_test_article(text_url="https://example.com/1"),
        make_test_article(text_url="https://example.com/2"),
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
            "extracted": 2 * len(RSS_SOURCES),
            "transformed": 2,
            "valid": 2,
            "loaded": 2,
        }

        assert mock_extract.call_count == len(RSS_SOURCES)
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
                *([[article] for _ in range(len(RSS_SOURCES) - 1)]),
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
        print(stats)
        assert stats == {
            "extracted": len(RSS_SOURCES) - 1,
            "transformed": 1,
            "valid": 1,
            "loaded": 1,
        }

        assert mock_extract.call_count == len(RSS_SOURCES)
        mock_transform.assert_called_once()
        mock_validate.assert_called_once()
        mock_load.assert_called_once()
        connection.close.assert_called_once()


@patch("src.pipeline.finish_pipeline_run")
@patch("src.pipeline.create_pipeline_run", return_value=42)
@patch("src.pipeline.try_create_connection")
@patch("src.pipeline.load_articles", return_value=2)
@patch("src.pipeline.validate_articles")
@patch("src.pipeline.transform_articles")
@patch("src.pipeline.extract_rss")
def test_run_pipeline_tracks_success(
    mock_extract,
    mock_transform,
    mock_validate,
    mock_load,
    mock_connection,
    mock_create_run,
    mock_finish_run,
):
    article = make_test_article()
    connection = MagicMock()

    mock_connection.return_value = connection
    mock_extract.return_value = [article]
    mock_transform.return_value = [article]
    mock_validate.return_value = [article]

    stats = run_pipeline()

    assert stats == {
        "extracted": len(RSS_SOURCES),
        "transformed": 1,
        "valid": 1,
        "loaded": 2,
    }

    mock_create_run.assert_called_once()
    mock_finish_run.assert_called_once()

    assert mock_finish_run.call_args.args[1] == 42
    assert mock_finish_run.call_args.args[3] == "success"

    connection.close.assert_called_once()


@patch("src.pipeline.finish_pipeline_run")
@patch("src.pipeline.create_pipeline_run", return_value=42)
@patch("src.pipeline.try_create_connection")
@patch("src.pipeline.transform_articles", side_effect=Exception("Transform failed"))
@patch("src.pipeline.extract_rss")
def test_run_pipeline_tracks_failure(
    mock_extract,
    mock_transform,
    mock_connection,
    mock_create_run,
    mock_finish_run,
):
    article = make_test_article()
    connection = MagicMock()

    mock_connection.return_value = connection
    mock_extract.return_value = [article]

    with pytest.raises(Exception, match="Transform failed"):
        run_pipeline()

    mock_create_run.assert_called_once()
    mock_finish_run.assert_called_once()

    assert mock_finish_run.call_args.args[1] == 42
    assert mock_finish_run.call_args.args[3] == "failed"
    assert mock_finish_run.call_args.args[4] == len(RSS_SOURCES)
    assert mock_finish_run.call_args.args[5] is None
    assert mock_finish_run.call_args.args[6] is None
    assert mock_finish_run.call_args.args[7] is None
    assert mock_finish_run.call_args.args[8] == "Transform failed"

    connection.close.assert_called_once()
