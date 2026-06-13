"""Bridged tool: get_mysql_slow_queries (from OpenSRE app.tools.MySQLSlowQueriesTool)."""

from __future__ import annotations

from typing import Any

from mysql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mysql_slow_queries',
    source='mysql',
    description='Retrieve slow MySQL queries from performance_schema, ranked by average execution time.',
    input_schema={'type': 'object', 'properties': {'threshold_ms': {'type': 'number'}, 'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying slow queries that may be causing performance degradation', 'Analyzing query execution patterns during incident timeframes', 'Finding poorly optimized queries with high execution times or full-table scans'],
)
def get_mysql_slow_queries(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MySQLSlowQueriesTool',
            attr='get_mysql_slow_queries',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mysql_slow_queries failed: {exc}"}
