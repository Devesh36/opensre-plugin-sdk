"""Bridged tool: call_openclaw_tool (from OpenSRE app.tools.OpenClawMCPTool)."""

from __future__ import annotations

from typing import Any

from openclaw_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='call_openclaw_tool',
    source='openclaw',
    description='Call a named tool exposed by the configured OpenClaw MCP bridge.',
    input_schema={'type': 'object', 'properties': {'tool_name': {'type': 'string'}, 'arguments': {'type': 'object'}, 'openclaw_url': {'type': 'string'}, 'openclaw_mode': {'type': 'string'}, 'openclaw_token': {'type': 'string'}, 'openclaw_command': {'type': 'string'}, 'openclaw_args': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['tool_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['tool_name'],
    use_cases=['Reading OpenClaw conversations and recent transcript history', 'Polling OpenClaw event queues or responding through an existing route'],
)
def call_openclaw_tool(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpenClawMCPTool',
            attr='call_openclaw_bridge_tool',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"call_openclaw_tool failed: {exc}"}
