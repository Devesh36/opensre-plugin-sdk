"""Validate every bundled plugin package."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from opensre_plugin.cli.main import main

PLUGINS = sorted(
    p
    for p in (Path(__file__).parent.parent / "plugins").iterdir()
    if p.is_dir() and p.name != "opensre_plugins"
)


def test_all_plugins_validate() -> None:
    runner = CliRunner()
    for plugin_path in PLUGINS:
        result = runner.invoke(main, ["validate", str(plugin_path)])
        assert result.exit_code == 0, f"{plugin_path.name}: {result.exception or result.output}"
