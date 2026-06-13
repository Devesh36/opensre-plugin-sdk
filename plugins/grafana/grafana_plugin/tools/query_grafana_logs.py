"""Bridged tool: query_grafana_logs (from OpenSRE app.tools.GrafanaLogsTool)."""

from __future__ import annotations

from typing import Any

from grafana_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_grafana_logs',
    source='grafana',
    description='Query Grafana Loki for pipeline logs.',
    input_schema={'type': 'object', 'properties': {'service_name': {'type': 'string'}, 'execution_run_id': {'type': 'string'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 100}, 'grafana_endpoint': {'type': 'string'}, 'grafana_api_key': {'type': 'string'}, 'grafana_username': {'type': 'string'}, 'grafana_password': {'type': 'string'}, 'pipeline_name': {'type': 'string'}}, 'required': ['service_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key'),
    requires=['service_name'],
    use_cases=['Retrieving application logs from Grafana Loki during an incident', 'Searching for error patterns in pipeline execution logs', 'Correlating log events with Grafana alert triggers'],
)
def query_grafana_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GrafanaLogsTool',
            attr='query_grafana_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_grafana_logs failed: {exc}"}
