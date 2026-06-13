"""Bridged tool: query_splunk_logs (from OpenSRE app.tools.SplunkSearchTool)."""

from __future__ import annotations

from typing import Any

from splunk_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_splunk_logs',
    source='splunk',
    description='Search Splunk using SPL (Search Processing Language) for application errors, exceptions, and operational events. Returns time-bounded log evidence.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string', 'description': "SPL search string (e.g. 'index=main error | head 50'). Do not include the leading 'search' keyword."}, 'time_range_minutes': {'type': 'integer', 'default': 60, 'description': 'Look-back window in minutes from now.'}, 'limit': {'type': 'integer', 'default': 50, 'description': 'Maximum number of events to return.'}, 'index': {'type': 'string', 'description': 'Splunk index to search (overrides integration default).'}}, 'required': ['query']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'token'),
    requires=[],
    use_cases=['Investigating application errors stored in Splunk', 'Searching Splunk indexes for error patterns during incident window', 'Fetching recent error logs for a service identified in an alert', 'Correlating trace IDs with Splunk log entries'],
)
def query_splunk_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SplunkSearchTool',
            attr='query_splunk_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_splunk_logs failed: {exc}"}
