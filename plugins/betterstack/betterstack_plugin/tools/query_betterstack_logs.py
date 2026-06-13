"""Bridged tool: query_betterstack_logs (from OpenSRE app.tools.BetterStackLogsTool)."""

from __future__ import annotations

from typing import Any

from betterstack_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_betterstack_logs',
    source='betterstack',
    description='Query a Better Stack Telemetry source for log rows using ClickHouse SQL over HTTP. Returns (dt, raw) pairs by UNIONing recent logs from remote(<source>_logs) with historical logs from s3Cluster(primary, <source>_s3) WHERE _row_type = 1, optionally bounded by since/until timestamps (ISO 8601).',
    input_schema={'type': 'object', 'properties': {'query_endpoint': {'type': 'string'}, 'sources': {'type': 'array', 'items': {'type': 'string'}}, 'source': {'type': 'string'}, 'since': {'type': 'string'}, 'until': {'type': 'string'}, 'limit': {'type': 'integer'}}, 'required': ['query_endpoint']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('username', 'password', 'endpoint'),
    requires=[],
    use_cases=['Fetching application log lines from a Better Stack source during RCA', 'Correlating timestamped log events with an alert window', 'Scanning a specific source (e.g. t123456_myapp) for recent and archived activity'],
)
def query_betterstack_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.BetterStackLogsTool',
            attr='query_betterstack_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_betterstack_logs failed: {exc}"}
