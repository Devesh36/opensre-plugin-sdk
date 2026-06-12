"""CLI validate command tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from opensre_plugin.cli.main import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_validate_passes_for_valid_fixture() -> None:
    result = CliRunner().invoke(main, ["validate", str(FIXTURES / "valid_plugin")])
    assert result.exit_code == 0, result.output
    assert "fixture_echo_tool" in result.output


def test_validate_fails_for_invalid_schema(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    plugin_root = tmp_path / "bad_plugin"
    plugin_root.mkdir()
    (plugin_root / "pyproject.toml").write_text(
        """
[tool.opensre-plugin]
name = "bad"
tools_package = "bad_plugin.tools"
""".strip(),
        encoding="utf-8",
    )
    pkg = plugin_root / "bad_plugin"
    pkg.mkdir()
    tools = pkg / "tools"
    tools.mkdir()
    (tools / "bad.py").write_text(
        """
from dataclasses import dataclass
from typing import Any

REGISTERED_TOOL_ATTR = "__opensre_registered_tool__"

@dataclass(frozen=True)
class Tool:
    name: str
    public_input_schema: dict[str, Any]

def fn():
    pass

setattr(fn, REGISTERED_TOOL_ATTR, Tool(
    name="bad_tool",
    public_input_schema={
        "type": "object",
        "properties": {"x": {"type": ["string", "null"]}},
    },
))
""",
        encoding="utf-8",
    )
    (tools / "__init__.py").write_text("", encoding="utf-8")

    monkeypatch.syspath_prepend(str(plugin_root))
    result = CliRunner().invoke(main, ["validate", str(plugin_root)])
    assert result.exit_code == 1
    assert "type must not be a list" in result.output
