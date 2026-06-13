#!/usr/bin/env bash
# Record a 30–60s terminal demo for the GitHub release.
#
# Option A — asciinema (recommended):
#   brew install asciinema   # or: pip install asciinema
#   asciinema rec -t demo.cast scripts/record_demo.sh
#
# Option B — run directly and screen-record your terminal:
#   ./scripts/record_demo.sh
#
# Attach demo.cast or your recording to the v0.1.0 GitHub release.

set -euo pipefail
cd "$(dirname "$0")/.."

export MOCK_API_KEY=demo

echo "=== opensre-plugin-sdk demo ==="
echo ""

echo "$ opensre-plugin validate plugins/mock"
uv run opensre-plugin validate plugins/mock
echo ""

echo "$ opensre-plugin validate plugins/linear"
uv run opensre-plugin validate plugins/linear
echo ""

echo "$ opensre-plugin validate (bad schema — expect failure)"
TMP=$(mktemp -d)
mkdir -p "$TMP/bad_plugin/bad_plugin/tools"
cat > "$TMP/bad_plugin/pyproject.toml" <<'TOML'
[tool.opensre-plugin]
name = "bad"
tools_package = "bad_plugin.tools"
TOML
cat > "$TMP/bad_plugin/bad_plugin/tools/bad.py" <<'PY'
from dataclasses import dataclass
REGISTERED_TOOL_ATTR = "__opensre_registered_tool__"
@dataclass(frozen=True)
class Tool:
    name: str
    public_input_schema: dict
def fn(): pass
setattr(fn, REGISTERED_TOOL_ATTR, Tool(
    name="bad_tool",
    public_input_schema={"type": "object", "properties": {"x": {"type": ["string", "null"]}}},
))
PY
touch "$TMP/bad_plugin/bad_plugin/__init__.py" "$TMP/bad_plugin/bad_plugin/tools/__init__.py"
PYTHONPATH="$TMP/bad_plugin" uv run opensre-plugin validate "$TMP/bad_plugin" || true
rm -rf "$TMP"
echo ""

echo "$ python scripts/demo_e2e.py"
uv run python scripts/demo_e2e.py
echo ""

echo "$ export MOCK_API_KEY=demo && python -c 'from mock_plugin import register; register()'"
export PYTHONPATH="plugins/mock:${PYTHONPATH:-}"
if python -c "import app.tools.registry" 2>/dev/null; then
  python -c "from mock_plugin import register; register(); from app.tools.registry import get_registered_tools; print([t.name for t in get_registered_tools('investigation') if 'mock' in t.name])"
else
  echo "(skipped — install opensre for registration step)"
fi
echo ""
echo "=== demo complete ==="
