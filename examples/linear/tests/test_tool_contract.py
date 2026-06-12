"""Linear plugin schema contract tests."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from opensre_plugin.cli.main import main
from opensre_plugin.schema.validator import validate_all_tools_in_module

from linear_plugin import tools


def test_tool_schemas_pass_strict_validator() -> None:
    assert validate_all_tools_in_module(tools) == []


def test_opensre_plugin_validate_passes() -> None:
    plugin_root = Path(__file__).resolve().parents[1]
    result = CliRunner().invoke(main, ["validate", str(plugin_root)])
    assert result.exit_code == 0, result.output
