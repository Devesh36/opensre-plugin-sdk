"""Bridged tool: get_mysql_server_status (from OpenSRE app.tools.MySQLServerStatusTool)."""

from __future__ import annotations

from typing import Any

from mysql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mysql_server_status',
    source='mysql',
    description='Retrieve MySQL server metrics including connections, uptime, query rates, and InnoDB buffer pool statistics.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Checking MySQL server health during an incident', 'Identifying connection saturation or exhaustion issues', 'Reviewing InnoDB buffer pool hit ratio and deadlock counts'],
)
def get_mysql_server_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MySQLServerStatusTool',
            attr='get_mysql_server_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mysql_server_status failed: {exc}"}
