"""Bridged tool: query_signoz_traces (from OpenSRE app.tools.SignozTracesTool)."""

from __future__ import annotations

from typing import Any

from signoz_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_signoz_traces',
    source='signoz',
    description='Query SigNoz traces for error rate, latency, and slow spans.',
    input_schema={'type': 'object', 'properties': {'service': {'type': 'string', 'description': 'Service name filter'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'error_only': {'type': 'boolean', 'default': False}, 'limit': {'type': 'integer', 'default': 50}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key'),
    requires=[],
    use_cases=['Investigating slow spans and error traces in SigNoz', 'Finding p99 latency bottlenecks by service', 'Correlating trace errors with logs and metrics'],
)
def query_signoz_traces(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SignozTracesTool',
            attr='query_signoz_traces',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_signoz_traces failed: {exc}"}
