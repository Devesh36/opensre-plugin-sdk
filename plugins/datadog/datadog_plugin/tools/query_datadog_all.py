"""Bridged tool: query_datadog_all (from OpenSRE app.tools.DataDogContextTool)."""

from __future__ import annotations

from typing import Any

from datadog_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_datadog_all',
    source='datadog',
    description='Fetch Datadog logs, monitors, and events in parallel for fast investigation.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'Datadog log search query'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 75}, 'monitor_query': {'type': 'string'}, 'kube_namespace': {'type': 'string'}}, 'required': ['query']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'app_key', 'site'),
    requires=[],
    use_cases=['Full Datadog context in a single fast operation', 'Kubernetes pod failure investigation (logs + monitors + events together)', 'Getting the complete picture for root cause analysis'],
)
def query_datadog_all(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DataDogContextTool',
            attr='fetch_datadog_context',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_datadog_all failed: {exc}"}
