"""Mock search tool for offline demos."""

from __future__ import annotations

from typing import Any

from mock_plugin.config import get_api_key
from opensre_plugin.decorators import plugin_tool


def _mock_available(sources: dict[str, dict]) -> bool:
    _ = sources
    return bool(get_api_key())


def _mock_extract_params(sources: dict[str, dict]) -> dict[str, Any]:
    _ = sources
    return {"api_key": get_api_key()}


@plugin_tool(
    name="search_mock_records",
    source="github",
    description="Search mock incident records by query (offline demo tool)",
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for mock records",
            },
        },
        "required": ["query"],
    },
    is_available=_mock_available,
    extract_params=_mock_extract_params,
    injected_params=("api_key",),
    requires=["api_key"],
    use_cases=[
        "Demo plugin registration without external APIs",
        "Test investigation tool schema validation offline",
    ],
)
def search_mock_records(query: str, api_key: str) -> dict[str, Any]:
    from mock_plugin.client import MockClient

    client = MockClient(api_key=api_key)
    return client.search(query=query)
