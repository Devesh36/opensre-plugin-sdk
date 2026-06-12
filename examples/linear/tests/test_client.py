"""Linear plugin tests."""

from __future__ import annotations

from linear_plugin.config import get_api_key
from linear_plugin.tools.search_issues import (
    _linear_available,
    _linear_extract_params,
    search_linear_issues,
)


def test_is_available_false_without_key(monkeypatch) -> None:
    monkeypatch.delenv("LINEAR_API_KEY", raising=False)
    assert _linear_available({}) is False


def test_extract_params_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("LINEAR_API_KEY", "lin_test")
    assert _linear_extract_params({}) == {"api_key": "lin_test"}
    assert get_api_key() == "lin_test"


def test_search_returns_error_on_api_failure(httpx_mock) -> None:
    httpx_mock.add_response(status_code=500)
    result = search_linear_issues("payment outage", api_key="lin_test")
    assert "error" in result
