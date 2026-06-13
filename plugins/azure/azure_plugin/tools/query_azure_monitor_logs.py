"""Bridged tool: query_azure_monitor_logs (from OpenSRE app.tools.AzureMonitorLogsTool)."""

from __future__ import annotations

from typing import Any

from azure_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_azure_monitor_logs',
    source='azure',
    description='Query Azure Monitor Log Analytics using a bounded KQL query.',
    input_schema={'type': 'object', 'properties': {'endpoint': {'type': 'string', 'default': 'https://api.loganalytics.io'}, 'query': {'type': 'string'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 50}, 'max_results': {'type': 'integer', 'default': 100}, 'integration_id': {'type': 'string'}, 'timeout_seconds': {'type': 'number', 'default': 20.0}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('workspace_id', 'access_token', 'token'),
    requires=['workspace_id', 'access_token'],
    use_cases=[],
)
def query_azure_monitor_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AzureMonitorLogsTool',
            attr='query_azure_monitor_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_azure_monitor_logs failed: {exc}"}
