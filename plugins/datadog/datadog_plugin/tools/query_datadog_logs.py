"""Bridged tool: query_datadog_logs (from OpenSRE app.tools.DataDogLogsTool)."""

from __future__ import annotations

from typing import Any

from datadog_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_datadog_logs',
    source='datadog',
    description='Search Datadog logs for pipeline errors, exceptions, and application events.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'Datadog log search query'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 50}}, 'required': ['query']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'app_key', 'site'),
    requires=[],
    use_cases=['Investigating pipeline errors reported by Datadog monitors', 'Finding error logs in Kubernetes namespaces', 'Searching for PIPELINE_ERROR patterns and ETL failures', 'Correlating log events with Datadog alerts'],
)
def query_datadog_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DataDogLogsTool',
            attr='query_datadog_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_datadog_logs failed: {exc}"}
