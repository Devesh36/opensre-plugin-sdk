"""Bridged tool: query_signoz_logs (from OpenSRE app.tools.SignozLogsTool)."""

from __future__ import annotations

from typing import Any

from signoz_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_signoz_logs',
    source='signoz',
    description='Query SigNoz logs by service, severity, and time window.',
    input_schema={'type': 'object', 'properties': {'service': {'type': 'string', 'description': 'Service name filter'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'severity': {'type': 'string', 'description': 'Severity filter (e.g. ERROR, WARN)'}, 'limit': {'type': 'integer', 'default': 50}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key'),
    requires=[],
    use_cases=['Investigating application errors reported by SigNoz alerts', 'Searching for error logs by service name and severity', 'Correlating log events with SigNoz trace spans'],
)
def query_signoz_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SignozLogsTool',
            attr='query_signoz_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_signoz_logs failed: {exc}"}
