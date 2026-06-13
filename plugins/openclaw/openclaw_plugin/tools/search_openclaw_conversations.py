"""Bridged tool: search_openclaw_conversations (from OpenSRE app.tools.OpenClawMCPTool)."""

from __future__ import annotations

from typing import Any

from openclaw_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='search_openclaw_conversations',
    source='openclaw',
    description='Search recent OpenClaw conversations through the configured MCP bridge.',
    input_schema={'type': 'object', 'properties': {'search': {'type': 'string'}, 'limit': {'type': 'integer'}, 'openclaw_url': {'type': 'string'}, 'openclaw_mode': {'type': 'string'}, 'openclaw_token': {'type': 'string'}, 'openclaw_command': {'type': 'string'}, 'openclaw_args': {'type': 'array', 'items': {'type': 'string'}}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=[],
    use_cases=['Checking whether an engineer already discussed the failing service in OpenClaw', 'Pulling recent OpenClaw context before querying external systems'],
)
def search_openclaw_conversations(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpenClawMCPTool',
            attr='search_openclaw_conversations',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"search_openclaw_conversations failed: {exc}"}
