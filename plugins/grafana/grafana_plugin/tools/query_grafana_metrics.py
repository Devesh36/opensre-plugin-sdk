"""Bridged tool: query_grafana_metrics (from OpenSRE app.tools.GrafanaMetricsTool)."""

from __future__ import annotations

from typing import Any

from grafana_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_grafana_metrics',
    source='grafana',
    description='Query Grafana Cloud Mimir for pipeline metrics.',
    input_schema={'properties': {'metric_name': {'description': 'Grafana Mimir metric query expression to execute.', 'examples': ['pipeline_runs_total', 'sum(rate(http_requests_total[5m]))'], 'type': 'string'}, 'service_name': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'description': 'Optional service filter applied by Grafana helper query wrappers.'}}, 'required': ['metric_name'], 'type': 'object', 'additionalProperties': False},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key'),
    requires=['metric_name'],
    use_cases=['Checking pipeline throughput and error rate metrics', 'Reviewing resource utilisation trends over time', 'Correlating metric anomalies with alert triggers'],
)
def query_grafana_metrics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GrafanaMetricsTool',
            attr='query_grafana_metrics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_grafana_metrics failed: {exc}"}
