"""Bridged tool: query_coralogix_logs (from OpenSRE app.tools.CoralogixLogsTool)."""

from __future__ import annotations

from typing import Any

from coralogix_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_coralogix_logs',
    source='coralogix',
    description='Query Coralogix DataPrime logs for error signatures and incident context.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 50}, 'application_name': {'type': 'string'}, 'subsystem_name': {'type': 'string'}, 'trace_id': {'type': 'string'}, 'coralogix_api_key': {'type': 'string'}, 'coralogix_base_url': {'type': 'string', 'default': 'https://api.coralogix.com'}}, 'required': ['query']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'base_url'),
    requires=[],
    use_cases=['Searching Coralogix logs for a failing service or subsystem', 'Looking up recent errors that match an alert message', 'Correlating a trace ID with recent Coralogix log events'],
)
def query_coralogix_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.CoralogixLogsTool',
            attr='query_coralogix_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_coralogix_logs failed: {exc}"}
