"""Bridged tool: get_error_logs (from OpenSRE app.tools.TracerErrorLogsTool)."""

from __future__ import annotations

from typing import Any

from tracer_web_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_error_logs',
    source='tracer_web',
    description='Get logs from OpenSearch, optionally filtered for errors.',
    input_schema={'type': 'object', 'properties': {'trace_id': {'type': 'string'}, 'size': {'type': 'integer', 'default': 500}, 'error_only': {'type': 'boolean', 'default': True}}, 'required': ['trace_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('jwt_token', 'api_url'),
    requires=['trace_id'],
    use_cases=['Proving error pattern hypothesis', 'Finding root cause error messages', 'Understanding failure timeline'],
)
def get_error_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerErrorLogsTool',
            attr='get_error_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_error_logs failed: {exc}"}
