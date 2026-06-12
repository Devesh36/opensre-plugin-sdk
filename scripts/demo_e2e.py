#!/usr/bin/env python3
"""End-to-end smoke test: validate, register, and verify Linear plugin tools."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINEAR_ROOT = ROOT / "examples" / "linear"


def main() -> int:
    if not LINEAR_ROOT.is_dir():
        print(f"ERROR: Linear example not found at {LINEAR_ROOT}", file=sys.stderr)
        return 1

    sys.path.insert(0, str(LINEAR_ROOT))

    from click.testing import CliRunner

    from opensre_plugin.cli.main import main as cli_main
    from opensre_plugin.loader import register_tools
    from opensre_plugin.schema.validator import validate_all_tools_in_module

    print("1/4  opensre-plugin validate examples/linear")
    result = CliRunner().invoke(cli_main, ["validate", str(LINEAR_ROOT)])
    if result.exit_code != 0:
        print(result.output, file=sys.stderr)
        return result.exit_code
    print(result.output.rstrip())

    print("\n2/4  Schema check on linear_plugin.tools")
    import linear_plugin.tools  # noqa: F401 — side-effect import for package
    from linear_plugin import tools

    errors = validate_all_tools_in_module(tools)
    if errors:
        for error in errors:
            print(f"  ERROR: {error}", file=sys.stderr)
        return 1
    print("  OK: search_linear_issues schema valid")

    try:
        import app.tools.registry  # noqa: F401
    except ImportError:
        print("\n3/4  Skipped registration (opensre not installed)")
        print("  Install opensre to complete the demo: uv pip install -e ../opensre")
        return 0

    from app.tools.registry import clear_tool_registry_cache, get_registered_tools

    os.environ.setdefault("LINEAR_API_KEY", "demo_key_for_e2e")
    clear_tool_registry_cache()
    register_tools(tools)

    print("\n3/4  register_tools(linear_plugin.tools)")
    investigation_tools = get_registered_tools("investigation")
    linear_tools = [tool for tool in investigation_tools if tool.name == "search_linear_issues"]
    if not linear_tools:
        print("  ERROR: search_linear_issues not in investigation registry", file=sys.stderr)
        return 1
    tool = linear_tools[0]
    print(f"  OK: registered {tool.name!r} (source={tool.source})")

    print("\n4/4  Tool availability + dry run")
    sources: dict[str, dict] = {}
    assert tool.is_available(sources), "expected tool available with LINEAR_API_KEY set"
    params = tool.extract_params(sources)
    assert params.get("api_key"), "extract_params should return api_key"

    # Call run() with a bogus key — should return {"error": ...}, not raise.
    result_payload = tool.run(query="payment outage", api_key="invalid_demo_key")
    if "error" in result_payload:
        err = str(result_payload["error"])[:80]
        print(f"  OK: run() returned error payload (expected without real API): {err}")
    elif result_payload.get("success"):
        print("  OK: run() succeeded (real Linear API key configured)")
    else:
        print(f"  WARN: unexpected payload keys: {list(result_payload.keys())}")

    print("\nDemo complete. To run a full investigation:")
    print("  export LINEAR_API_KEY=lin_api_xxx")
    print('  python -c "from linear_plugin import register; register()"')
    print("  opensre investigate --alert '{\"title\": \"Payment API 500 errors\"}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
