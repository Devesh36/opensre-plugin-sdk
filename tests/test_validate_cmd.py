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


def test_validate_fails_for_missing_manifest_table(tmp_path: Path) -> None:
    plugin_root = tmp_path / "no_manifest"
    plugin_root.mkdir()
    (plugin_root / "pyproject.toml").write_text('[project]\nname = "demo"\n', encoding="utf-8")

    result = CliRunner().invoke(main, ["validate", str(plugin_root)])
    assert result.exit_code == 1
    assert "Missing [tool.opensre-plugin]" in result.output


def test_validate_fails_for_missing_required_name(tmp_path: Path) -> None:
    plugin_root = tmp_path / "no_name"
    plugin_root.mkdir()
    (plugin_root / "pyproject.toml").write_text(
        '[tool.opensre-plugin]\ntools_package = "pkg.tools"\n',
        encoding="utf-8",
    )

    result = CliRunner().invoke(main, ["validate", str(plugin_root)])
    assert result.exit_code == 1
    assert "name is required" in result.output


def test_validate_fails_for_duplicate_tool_names(tmp_path: Path) -> None:
    plugin_root = tmp_path / "dup_plugin"
    plugin_root.mkdir()
    (plugin_root / "pyproject.toml").write_text(
        """
[tool.opensre-plugin]
name = "dup"
tools_package = "dup_plugin.tools"
""".strip(),
        encoding="utf-8",
    )
    pkg = plugin_root / "dup_plugin"
    tools = pkg / "tools"
    tools.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (tools / "__init__.py").write_text("", encoding="utf-8")

    tool_stub = '''
from dataclasses import dataclass
from typing import Any

REGISTERED_TOOL_ATTR = "__opensre_registered_tool__"

@dataclass(frozen=True)
class Tool:
    name: str
    public_input_schema: dict[str, Any]

def make_tool():
    def fn() -> None:
        pass
    setattr(fn, REGISTERED_TOOL_ATTR, Tool(
        name="same_name",
        public_input_schema={
            "type": "object",
            "properties": {"q": {"type": "string"}},
            "required": ["q"],
        },
    ))
    return fn
'''
    (tools / "one.py").write_text(f"{tool_stub}\none_fn = make_tool()\n", encoding="utf-8")
    (tools / "two.py").write_text(f"{tool_stub}\ntwo_fn = make_tool()\n", encoding="utf-8")

    result = CliRunner().invoke(main, ["validate", str(plugin_root)])
    assert result.exit_code == 1
    assert "duplicate tool name 'same_name'" in result.output
