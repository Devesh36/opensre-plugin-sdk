"""Bridged tool: query_datadog_monitors (from OpenSRE app.tools.DataDogMonitorsTool)."""

from __future__ import annotations

from typing import Any

from datadog_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_datadog_monitors',
    source='datadog',
    description='List Datadog monitors to understand alerting configuration and current states.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string', 'description': "Optional monitor filter (e.g., 'tag:pipeline:tracer-ai-agent')"}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'app_key', 'site'),
    requires=[],
    use_cases=['Understanding which monitors triggered an alert', 'Finding the exact query behind a Datadog alert', 'Checking monitor states (OK, Alert, Warn, No Data)', 'Reviewing monitor configuration for pipeline monitoring'],
)
def query_datadog_monitors(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DataDogMonitorsTool',
            attr='query_datadog_monitors',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_datadog_monitors failed: {exc}"}
