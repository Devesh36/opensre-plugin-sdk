"""Bridged tool: get_mysql_replication_status (from OpenSRE app.tools.MySQLReplicationStatusTool)."""

from __future__ import annotations

from typing import Any

from mysql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mysql_replication_status',
    source='mysql',
    description='Retrieve MySQL replication status including IO/SQL thread health and replica lag.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Checking replica lag during high-write incidents', 'Verifying replication IO and SQL threads are running', 'Diagnosing replication errors and identifying last error details'],
)
def get_mysql_replication_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MySQLReplicationStatusTool',
            attr='get_mysql_replication_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mysql_replication_status failed: {exc}"}
