"""Bridged tool: query_grafana_service_names (from OpenSRE app.tools.GrafanaServiceNamesTool)."""

from __future__ import annotations

from typing import Any

from grafana_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_grafana_service_names',
    source='grafana',
    description='Discover available service names in Loki.',
    input_schema={'type': 'object', 'properties': {'grafana_endpoint': {'type': 'string'}, 'grafana_api_key': {'type': 'string'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key'),
    requires=[],
    use_cases=['Finding the correct service_name label when query_grafana_logs returns no results', 'Listing all services that have log data in Grafana Loki'],
)
def query_grafana_service_names(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GrafanaServiceNamesTool',
            attr='query_grafana_service_names',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_grafana_service_names failed: {exc}"}
