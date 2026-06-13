"""Bridged tool: query_signoz_metrics (from OpenSRE app.tools.SignozMetricsTool)."""

from __future__ import annotations

from typing import Any

from signoz_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_signoz_metrics',
    source='signoz',
    description='Query SigNoz metrics (CPU, memory, request rate) by service and time window.',
    input_schema={'type': 'object', 'properties': {'metric_name': {'type': 'string', 'description': 'Metric name: cpu_usage, memory_usage, request_rate, or a raw metric name. For error-rate semantics use query_signoz_traces instead.'}, 'service': {'type': 'string', 'description': 'Service name filter'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'aggregation': {'type': 'string', 'default': 'avg', 'description': 'avg, sum, max, min, count'}, 'limit': {'type': 'integer', 'default': 50}}, 'required': ['metric_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key'),
    requires=['metric_name'],
    use_cases=['Checking CPU and memory usage from SigNoz metrics', 'Reviewing request throughput by service', 'Correlating metric anomalies with SigNoz alerts'],
)
def query_signoz_metrics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SignozMetricsTool',
            attr='query_signoz_metrics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_signoz_metrics failed: {exc}"}
