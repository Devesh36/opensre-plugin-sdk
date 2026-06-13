"""Bridged tool: get_clickhouse_query_activity (from OpenSRE app.tools.ClickHouseQueryActivityTool)."""

from __future__ import annotations

from typing import Any

from clickhouse_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_clickhouse_query_activity',
    source='clickhouse',
    description='Retrieve recent query activity from a ClickHouse instance, including query duration, rows read, and memory usage.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}, 'username': {'type': 'string'}, 'secure': {'type': 'boolean'}, 'limit': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'password', 'user'),
    requires=[],
    use_cases=['Identifying slow or resource-heavy queries during an incident', 'Checking recent query patterns that may correlate with performance issues', 'Reviewing query activity after an alert fires'],
)
def get_clickhouse_query_activity(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.ClickHouseQueryActivityTool',
            attr='get_clickhouse_query_activity',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_clickhouse_query_activity failed: {exc}"}
