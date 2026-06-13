"""Bridged tool: get_host_metrics (from OpenSRE app.tools.TracerHostMetricsTool)."""

from __future__ import annotations

from typing import Any

from cloudwatch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_host_metrics',
    source='cloudwatch',
    description='Get host-level metrics (CPU, memory, disk) for the run.',
    input_schema={'type': 'object', 'properties': {'trace_id': {'type': 'string'}}, 'required': ['trace_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['trace_id'],
    use_cases=['Proving resource constraint hypothesis', 'Identifying memory/CPU exhaustion', 'Understanding infrastructure bottlenecks'],
)
def get_host_metrics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerHostMetricsTool',
            attr='get_host_metrics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_host_metrics failed: {exc}"}
