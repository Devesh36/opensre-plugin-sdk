"""Bridged tool: query_datadog_metrics (from OpenSRE app.tools.DataDogMetricsTool)."""

from __future__ import annotations

from typing import Any

from datadog_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_datadog_metrics',
    source='datadog',
    description='Query Datadog metrics for infrastructure and application performance data.',
    input_schema={'properties': {'metric_name': {'description': 'Datadog metric name to query, for example `system.cpu.user`.', 'type': 'string'}, 'time_range_minutes': {'default': 60, 'description': 'Lookback window in minutes for metric retrieval.', 'type': 'integer'}, 'query': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'description': 'Optional full Datadog metrics query string override.'}}, 'required': ['metric_name'], 'type': 'object', 'additionalProperties': False},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'app_key', 'site'),
    requires=[],
    use_cases=['Investigating CPU or memory spikes correlated with an alert', 'Reviewing custom pipeline throughput metrics over time', 'Checking host resource utilisation trends'],
)
def query_datadog_metrics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DataDogMetricsTool',
            attr='query_datadog_metrics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_datadog_metrics failed: {exc}"}
