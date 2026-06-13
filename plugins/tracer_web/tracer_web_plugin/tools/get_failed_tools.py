"""Bridged tool: get_failed_tools (from OpenSRE app.tools.TracerFailedToolsTool)."""

from __future__ import annotations

from typing import Any

from tracer_web_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_failed_tools',
    source='tracer_web',
    description='Get tools that failed during a pipeline execution.',
    input_schema={'type': 'object', 'properties': {'trace_id': {'type': 'string'}}, 'required': ['trace_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('jwt_token', 'api_url'),
    requires=['trace_id'],
    use_cases=['Proving tool failure hypothesis', 'Identifying specific failing components', 'Understanding error patterns in tool execution'],
)
def get_failed_tools(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerFailedToolsTool',
            attr='get_failed_tools',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_failed_tools failed: {exc}"}
