"""``opensre-plugin init`` tests."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from click.testing import CliRunner

from opensre_plugin.cli.main import main
from opensre_plugin.loader import list_plugin_tools
from opensre_plugin.manifest import import_tools_package, load_manifest


def test_init_generates_expected_tree(tmp_path: Path) -> None:
    result = CliRunner().invoke(main, ["init", "mytool", "--output", str(tmp_path)])
    assert result.exit_code == 0, result.output

    plugin_root = tmp_path / "mytool_plugin"
    assert (plugin_root / "pyproject.toml").is_file()
    assert (plugin_root / "README.md").is_file()
    assert (plugin_root / "mytool_plugin" / "__init__.py").is_file()
    assert (plugin_root / "mytool_plugin" / "client.py").is_file()
    assert (plugin_root / "mytool_plugin" / "config.py").is_file()
    assert (plugin_root / "mytool_plugin" / "tools" / "__init__.py").is_file()
    assert (plugin_root / "mytool_plugin" / "tools" / "mytool.py").is_file()
    assert (plugin_root / "tests" / "test_tool_contract.py").is_file()

    pyproject = (plugin_root / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "mytool"' in pyproject
    assert 'tools_package = "mytool_plugin.tools"' in pyproject

    tool_source = (plugin_root / "mytool_plugin" / "tools" / "mytool.py").read_text(
        encoding="utf-8"
    )
    assert "search_mytool" in tool_source
    assert "MYTOOL_API_KEY" in (plugin_root / "mytool_plugin" / "config.py").read_text(
        encoding="utf-8"
    )

    validate = CliRunner().invoke(main, ["validate", str(plugin_root)])
    assert validate.exit_code == 0, validate.output
    assert "search_mytool" in validate.output


def test_init_generates_importable_package(tmp_path: Path) -> None:
    """Scaffolded plugin must import without pip install -e (validate path)."""
    result = CliRunner().invoke(main, ["init", "acme", "--output", str(tmp_path)])
    assert result.exit_code == 0, result.output

    plugin_root = tmp_path / "acme_plugin"
    manifest = load_manifest(plugin_root)
    assert manifest.tools_package == "acme_plugin.tools"

    tools_module = import_tools_package(manifest)
    assert list_plugin_tools(tools_module) == ["search_acme"]

    # Regression: register() entry point imports cleanly.
    root = str(plugin_root.resolve())
    if root not in sys.path:
        sys.path.insert(0, root)
    register_mod = importlib.import_module("acme_plugin")
    assert callable(register_mod.register)
