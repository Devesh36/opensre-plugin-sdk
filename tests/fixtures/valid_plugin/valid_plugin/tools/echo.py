"""Echo tool for offline validation fixture tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

REGISTERED_TOOL_ATTR = "__opensre_registered_tool__"


@dataclass(frozen=True)
class _FixtureTool:
    name: str
    public_input_schema: dict[str, Any]
    source: str = "github"


def fixture_echo_tool(query: str) -> dict[str, Any]:
    return {"success": True, "query": query}


setattr(
    fixture_echo_tool,
    REGISTERED_TOOL_ATTR,
    _FixtureTool(
        name="fixture_echo_tool",
        public_input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Echo input"},
            },
            "required": ["query"],
        },
    ),
)
