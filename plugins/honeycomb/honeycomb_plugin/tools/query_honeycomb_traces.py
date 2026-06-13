"""Bridged tool: query_honeycomb_traces (from OpenSRE app.tools.HoneycombTracesTool)."""

from __future__ import annotations

from typing import Any

from honeycomb_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_honeycomb_traces',
    source='honeycomb',
    description='Query Honeycomb for trace/span groups related to an incident.',
    input_schema={'type': 'object', 'properties': {'service_name': {'type': 'string'}, 'trace_id': {'type': 'string'}, 'time_range_seconds': {'type': 'integer', 'default': 3600}, 'limit': {'type': 'integer', 'default': 20}, 'honeycomb_api_key': {'type': 'string'}, 'honeycomb_base_url': {'type': 'string', 'default': 'https://api.honeycomb.io'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('dataset', 'api_key', 'base_url'),
    requires=[],
    use_cases=['Investigating failing or slow distributed traces in Honeycomb', 'Looking up spans for a specific trace ID', 'Checking whether one service is producing anomalous spans during an incident'],
)
def query_honeycomb_traces(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.HoneycombTracesTool',
            attr='query_honeycomb_traces',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_honeycomb_traces failed: {exc}"}
