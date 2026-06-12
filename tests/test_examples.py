"""Validate bundled example plugins."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from opensre_plugin.cli.main import main

EXAMPLES = Path(__file__).parent.parent / "examples"


def test_validate_linear_example() -> None:
    result = CliRunner().invoke(main, ["validate", str(EXAMPLES / "linear")])
    assert result.exit_code == 0, result.output
    assert "search_linear_issues" in result.output


def test_validate_mock_example() -> None:
    result = CliRunner().invoke(main, ["validate", str(EXAMPLES / "mock")])
    assert result.exit_code == 0, result.output
    assert "search_mock_records" in result.output
