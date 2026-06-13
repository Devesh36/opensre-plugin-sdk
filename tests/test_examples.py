"""Validate bundled integration plugins."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from opensre_plugin.cli.main import main

PLUGINS = Path(__file__).parent.parent / "plugins"


def test_validate_linear_plugin() -> None:
    result = CliRunner().invoke(main, ["validate", str(PLUGINS / "linear")])
    assert result.exit_code == 0, result.output
    assert "search_linear_issues" in result.output


def test_validate_mock_plugin() -> None:
    result = CliRunner().invoke(main, ["validate", str(PLUGINS / "mock")])
    assert result.exit_code == 0, result.output
    assert "search_mock_records" in result.output
