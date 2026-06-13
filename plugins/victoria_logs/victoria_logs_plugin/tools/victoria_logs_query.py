"""Bridged tool: victoria_logs_query (from OpenSRE app.tools.VictoriaLogsTool)."""

from __future__ import annotations

from typing import Any

from victoria_logs_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='victoria_logs_query',
    source='victoria_logs',
    description='Query structured logs from VictoriaLogs using LogsQL to investigate application errors, request anomalies, or other log-correlated signals.',
    input_schema={'type': 'object', 'properties': {'base_url': {'type': 'string', 'description': 'VictoriaLogs base URL (e.g. http://vmlogs:9428)'}, 'query': {'type': 'string', 'default': '*', 'description': 'LogsQL query string (e.g. `_stream_id:* AND error`). Defaults to the wildcard `*`; alert-derived query targeting through the executor path is a known follow-up.'}, 'limit': {'type': 'integer', 'default': 50, 'description': 'Maximum number of log entries to return.'}, 'start': {'type': 'string', 'default': '-1h', 'description': 'Time range expression accepted by VictoriaLogs (e.g. -1h, -24h).'}}, 'required': ['base_url']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('tenant_id', 'url'),
    requires=['base_url'],
    use_cases=['Investigating application logs for errors related to a firing alert', 'Filtering structured log streams by service, level, or trace ID', 'Correlating recent log volume changes with an incident timeline'],
)
def victoria_logs_query(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.VictoriaLogsTool',
            attr='victoria_logs_query',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"victoria_logs_query failed: {exc}"}
