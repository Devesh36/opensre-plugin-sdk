"""Bridged tool: get_azure_sql_slow_queries (from OpenSRE app.tools.AzureSQLSlowQueriesTool)."""

from __future__ import annotations

from typing import Any

from azure_sql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_azure_sql_slow_queries',
    source='azure_sql',
    description='Retrieve slow query statistics from Azure SQL Database query stats DMV, ordered by average elapsed time.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}, 'threshold_ms': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('server', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying queries with high average execution time', 'Finding resource-intensive queries causing DTU throttling', 'Reviewing query performance trends for capacity planning'],
)
def get_azure_sql_slow_queries(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AzureSQLSlowQueriesTool',
            attr='get_azure_sql_slow_queries',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_azure_sql_slow_queries failed: {exc}"}
