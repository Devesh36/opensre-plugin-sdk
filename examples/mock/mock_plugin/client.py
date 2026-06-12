"""In-memory mock client — no HTTP."""

from __future__ import annotations

from typing import Any


class MockClient:
    def __init__(self, *, api_key: str) -> None:
        self._api_key = api_key

    def search(self, query: str) -> dict[str, Any]:
        if not self._api_key:
            return {"error": "MOCK_API_KEY is not configured"}
        return {
            "success": True,
            "records": [
                {
                    "id": "mock-1",
                    "title": f"Mock record matching: {query}",
                }
            ],
        }
