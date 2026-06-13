"""Bridged tool: get_clickhouse_system_health (from OpenSRE app.tools.ClickHouseSystemHealthTool)."""

from __future__ import annotations

from typing import Any

from clickhouse_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_clickhouse_system_health',
    source='clickhouse',
    description='Retrieve system health metrics and table statistics from a ClickHouse instance, including active queries, connections, and table sizes.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}, 'username': {'type': 'string'}, 'secure': {'type': 'boolean'}, 'include_table_stats': {'type': 'boolean'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'password', 'user'),
    requires=[],
    use_cases=['Checking ClickHouse server health during an incident', 'Identifying large or rapidly growing tables', 'Reviewing connection and query counts for capacity issues'],
)
def get_clickhouse_system_health(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.ClickHouseSystemHealthTool',
            attr='get_clickhouse_system_health',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_clickhouse_system_health failed: {exc}"}
