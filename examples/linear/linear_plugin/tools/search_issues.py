"""Search Linear issues for incident correlation."""

from __future__ import annotations

from typing import Any

from linear_plugin.config import get_api_key
from opensre_plugin.decorators import plugin_tool


def _linear_available(sources: dict[str, dict]) -> bool:
    _ = sources
    return bool(get_api_key())


def _linear_extract_params(sources: dict[str, dict]) -> dict[str, Any]:
    _ = sources
    return {"api_key": get_api_key()}


@plugin_tool(
    name="search_linear_issues",
    source="github",
    description="Search Linear issues by query string for incident correlation",
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for Linear issues",
            },
        },
        "required": ["query"],
    },
    is_available=_linear_available,
    extract_params=_linear_extract_params,
    injected_params=("api_key",),
    requires=["api_key"],
    use_cases=[
        "Find related bugs when investigating production errors",
        "Correlate alert with known Linear issues",
    ],
)
def search_linear_issues(query: str, api_key: str) -> dict[str, Any]:
    from linear_plugin.client import LinearClient

    client = LinearClient(api_key=api_key)
    return client.search_issues(query=query)
