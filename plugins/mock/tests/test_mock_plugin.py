"""Mock plugin tests."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner
from mock_plugin import tools
from mock_plugin.tools.search_records import _mock_available, search_mock_records

from opensre_plugin.cli.main import main
from opensre_plugin.schema.validator import validate_all_tools_in_module


def test_is_available_without_key(monkeypatch) -> None:
    monkeypatch.delenv("MOCK_API_KEY", raising=False)
    assert _mock_available({}) is False


def test_search_returns_success(monkeypatch) -> None:
    monkeypatch.setenv("MOCK_API_KEY", "demo")
    result = search_mock_records("outage", api_key="demo")
    assert result["success"] is True
    assert result["records"][0]["title"] == "Mock record matching: outage"


def test_validate_passes() -> None:
    assert validate_all_tools_in_module(tools) == []


def test_cli_validate_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    result = CliRunner().invoke(main, ["validate", str(root)])
    assert result.exit_code == 0, result.output
