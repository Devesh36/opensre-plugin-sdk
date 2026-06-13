"""Bridged tool: query_datadog_events (from OpenSRE app.tools.DataDogEventsTool)."""

from __future__ import annotations

from typing import Any

from datadog_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_datadog_events',
    source='datadog',
    description='Query Datadog events for deployments, alerts, and system changes.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'Event search query'}, 'time_range_minutes': {'type': 'integer', 'default': 60}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'app_key', 'site'),
    requires=[],
    use_cases=['Finding recent deployment events that may correlate with failures', 'Reviewing alert trigger/resolve events', 'Checking for infrastructure changes around the time of an incident'],
)
def query_datadog_events(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DataDogEventsTool',
            attr='query_datadog_events',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_datadog_events failed: {exc}"}
