from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from src.repository.pipeline_runs import (
    create_pipeline_run,
    finish_pipeline_run,
    get_pipeline_runs,
)


def test_create_pipeline_run():
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = (42,)

    started_at = datetime.now(timezone.utc)

    result = create_pipeline_run(connection, started_at)

    assert result == 42
    cursor.execute.assert_called_once()
    connection.commit.assert_called_once()


def test_create_pipeline_run_raises_if_no_id():
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = None

    started_at = datetime.now(timezone.utc)

    with pytest.raises(RuntimeError, match="Failed to create pipeline run"):
        create_pipeline_run(connection, started_at)


def test_finish_pipeline_run():
    connection = MagicMock()

    finished_at = datetime.now(timezone.utc)

    finish_pipeline_run(
        connection,
        run_id=42,
        finished_at=finished_at,
        status="success",
        extracted=201,
        transformed=185,
        valid=184,
        loaded=42,
    )

    cursor = connection.cursor.return_value.__enter__.return_value

    cursor.execute.assert_called_once()
    connection.commit.assert_called_once()


def test_finish_pipeline_run_with_error():
    connection = MagicMock()

    finished_at = datetime.now(timezone.utc)

    finish_pipeline_run(
        connection,
        run_id=42,
        finished_at=finished_at,
        status="failed",
        extracted=201,
        transformed=185,
        valid=None,
        loaded=None,
        error="Validation failed",
    )

    cursor = connection.cursor.return_value.__enter__.return_value

    cursor.execute.assert_called_once()
    connection.commit.assert_called_once()


def test_get_pipeline_runs():
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value

    expected = [
        (
            2,
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
            "success",
            201,
            185,
            42,
            None,
        )
    ]

    cursor.fetchall.return_value = expected

    result = get_pipeline_runs(
        connection,
        limit=20,
        offset=0,
    )

    assert result == expected
    cursor.execute.assert_called_once()
