"""Bridged tool: get_batch_statistics (from OpenSRE app.tools.TracerBatchStatisticsTool)."""

from __future__ import annotations

from typing import Any

from tracer_web_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_batch_statistics',
    source='tracer_web',
    description='Get batch job statistics for a specific trace.',
    input_schema={'type': 'object', 'properties': {'trace_id': {'type': 'string'}}, 'required': ['trace_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('jwt_token', 'api_url'),
    requires=['trace_id'],
    use_cases=['Proving systemic failure hypothesis (high failure rate)', 'Understanding overall job execution patterns', 'Cost analysis for pipeline runs'],
)
def get_batch_statistics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerBatchStatisticsTool',
            attr='get_batch_statistics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_batch_statistics failed: {exc}"}
