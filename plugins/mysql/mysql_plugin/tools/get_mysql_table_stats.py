"""Bridged tool: get_mysql_table_stats (from OpenSRE app.tools.MySQLTableStatsTool)."""

from __future__ import annotations

from typing import Any

from mysql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mysql_table_stats',
    source='mysql',
    description='Retrieve MySQL table statistics including row counts and data/index sizes from information_schema.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying the largest tables consuming storage during capacity incidents', 'Reviewing table sizes and growth patterns for capacity planning', 'Finding tables with unexpectedly high row counts or index overhead'],
)
def get_mysql_table_stats(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MySQLTableStatsTool',
            attr='get_mysql_table_stats',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mysql_table_stats failed: {exc}"}
