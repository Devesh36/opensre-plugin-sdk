"""Bridged tool: list_openclaw_tools (from OpenSRE app.tools.OpenClawMCPTool)."""

from __future__ import annotations

from typing import Any

from openclaw_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_openclaw_tools',
    source='openclaw',
    description='List tools exposed by the configured OpenClaw MCP bridge.',
    input_schema={'type': 'object', 'properties': {'openclaw_url': {'type': 'string'}, 'openclaw_mode': {'type': 'string'}, 'openclaw_token': {'type': 'string'}, 'openclaw_command': {'type': 'string'}, 'openclaw_args': {'type': 'array', 'items': {'type': 'string'}}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=[],
    use_cases=['Inspecting which OpenClaw bridge tools are available before making a call', 'Confirming whether conversation, event, or permissions tools are exposed'],
)
def list_openclaw_tools(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpenClawMCPTool',
            attr='list_openclaw_bridge_tools',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_openclaw_tools failed: {exc}"}
