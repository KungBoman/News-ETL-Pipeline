import pytest

from src.common_util import get_required_env


def test_get_required_env():
    assert get_required_env("DB_HOST") == "localhost"


def test_get_required_env_missing(monkeypatch):
    monkeypatch.delenv("TEST_MISSING_VARIABLE", raising=False)

    with pytest.raises(
        RuntimeError,
        match="Missing required environment variable: TEST_MISSING_VARIABLE",
    ):
        get_required_env("TEST_MISSING_VARIABLE")
