import pytest

from src.common_util import get_required_env


def test_get_required_env():
    monkeypatch.setenv("DB_HOST", "localhost")

    assert get_required_env("DB_HOST") == "localhost"


def test_get_required_env_missing(monkeypatch):
    monkeypatch.delenv("TEST_MISSING_VARIABLE", raising=False)

    with pytest.raises(
        RuntimeError,
        match="Missing required environment variable: TEST_MISSING_VARIABLE",
    ):
        get_required_env("TEST_MISSING_VARIABLE")


def test_get_required_env_raises_when_missing(monkeypatch):
    monkeypatch.delenv("DB_HOST", raising=False)

    with pytest.raises(
        RuntimeError,
        match="Missing required environment variable: DB_HOST",
    ):
        get_required_env("DB_HOST")
