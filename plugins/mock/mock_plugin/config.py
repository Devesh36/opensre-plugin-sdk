"""Mock plugin configuration."""

from __future__ import annotations

import os


def get_api_key() -> str:
    return os.environ.get("MOCK_API_KEY", "")
