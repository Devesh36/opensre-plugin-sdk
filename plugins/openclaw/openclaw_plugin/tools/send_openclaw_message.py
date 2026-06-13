"""Bridged tool: send_openclaw_message (from OpenSRE app.tools.OpenClawMCPTool)."""

from __future__ import annotations

from typing import Any

from openclaw_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='send_openclaw_message',
    source='openclaw',
    description='Send a message into an existing OpenClaw conversation.',
    input_schema={'type': 'object', 'properties': {'conversation_id': {'type': 'string'}, 'content': {'type': 'string'}, 'openclaw_url': {'type': 'string'}, 'openclaw_mode': {'type': 'string'}, 'openclaw_token': {'type': 'string'}, 'openclaw_command': {'type': 'string'}, 'openclaw_args': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['conversation_id', 'content']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['conversation_id'],
    use_cases=['Writing investigation findings back into a conversation an engineer is already using', 'Appending a short remediation note or next-step summary to an OpenClaw thread'],
)
def send_openclaw_message(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpenClawMCPTool',
            attr='send_openclaw_message',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"send_openclaw_message failed: {exc}"}
