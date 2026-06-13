"""Linear plugin configuration."""

from __future__ import annotations

import os


def get_api_key() -> str:
    return os.environ.get("LINEAR_API_KEY", "")
