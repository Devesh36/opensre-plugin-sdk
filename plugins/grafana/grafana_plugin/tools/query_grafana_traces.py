"""Bridged tool: query_grafana_traces (from OpenSRE app.tools.GrafanaTracesTool)."""

from __future__ import annotations

from typing import Any

from grafana_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_grafana_traces',
    source='grafana',
    description='Query Grafana Cloud Tempo for pipeline traces.',
    input_schema={'type': 'object', 'properties': {'service_name': {'type': 'string'}, 'execution_run_id': {'type': 'string'}, 'limit': {'type': 'integer', 'default': 20}, 'grafana_endpoint': {'type': 'string'}, 'grafana_api_key': {'type': 'string'}}, 'required': ['service_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key'),
    requires=['service_name'],
    use_cases=['Tracing distributed request flows during a pipeline failure', 'Identifying slow spans or timeout patterns', 'Correlating trace data with log errors'],
)
def query_grafana_traces(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GrafanaTracesTool',
            attr='query_grafana_traces',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_grafana_traces failed: {exc}"}
