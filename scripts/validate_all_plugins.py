#!/usr/bin/env python3
"""Validate every plugin under plugins/."""

from __future__ import annotations

import sys
from pathlib import Path

from click.testing import CliRunner

from opensre_plugin.cli.main import main as cli_main

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = sorted(
    p
    for p in (ROOT / "plugins").iterdir()
    if p.is_dir() and p.name != "opensre_plugins"
)


def main() -> int:
    runner = CliRunner()
    failed: list[str] = []
    for plugin_path in PLUGINS:
        result = runner.invoke(cli_main, ["validate", str(plugin_path)])
        if result.exit_code != 0:
            failed.append(plugin_path.name)
            print(result.output, file=sys.stderr)
            if result.exception is not None:
                print(result.exception, file=sys.stderr)
    print(f"Validated {len(PLUGINS) - len(failed)}/{len(PLUGINS)} plugins")
    if failed:
        print("Failed:", ", ".join(failed), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
