"""Bridged tool: get_openclaw_conversation (from OpenSRE app.tools.OpenClawMCPTool)."""

from __future__ import annotations

from typing import Any

from openclaw_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_openclaw_conversation',
    source='openclaw',
    description='Fetch one OpenClaw conversation by id through the configured MCP bridge.',
    input_schema={'type': 'object', 'properties': {'conversation_id': {'type': 'string'}, 'openclaw_url': {'type': 'string'}, 'openclaw_mode': {'type': 'string'}, 'openclaw_token': {'type': 'string'}, 'openclaw_command': {'type': 'string'}, 'openclaw_args': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['conversation_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['conversation_id'],
    use_cases=['Reading the full context of an OpenClaw conversation that may explain the active alert', 'Pulling the latest assistant and engineer messages before continuing an investigation'],
)
def get_openclaw_conversation(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpenClawMCPTool',
            attr='get_openclaw_conversation',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_openclaw_conversation failed: {exc}"}
