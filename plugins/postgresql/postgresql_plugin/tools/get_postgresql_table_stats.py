"""Bridged tool: get_postgresql_table_stats (from OpenSRE app.tools.PostgreSQLTableStatsTool)."""

from __future__ import annotations

from typing import Any

from postgresql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_postgresql_table_stats',
    source='postgresql',
    description='Retrieve PostgreSQL table statistics including size, row counts, index usage, and maintenance info.',
    input_schema={'type': 'object', 'properties': {'schema_name': {'type': 'string'}, 'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying large tables or rapid table growth during storage incidents', 'Analyzing table scan patterns and index usage efficiency', 'Checking table maintenance status like vacuum and analyze operations'],
)
def get_postgresql_table_stats(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.PostgreSQLTableStatsTool',
            attr='get_postgresql_table_stats',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_postgresql_table_stats failed: {exc}"}
