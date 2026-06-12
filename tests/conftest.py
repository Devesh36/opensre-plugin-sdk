"""Pytest configuration."""

from __future__ import annotations

import sys
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
VALID_PLUGIN_ROOT = FIXTURES / "valid_plugin"
EXAMPLES_LINEAR = Path(__file__).parent.parent / "examples" / "linear"

for path in (VALID_PLUGIN_ROOT, EXAMPLES_LINEAR):
    if path.is_dir():
        sys.path.insert(0, str(path))
