"""Bridged tool: get_mariadb_innodb_status (from OpenSRE app.tools.MariaDBInnoDBStatusTool)."""

from __future__ import annotations

from typing import Any

from mariadb_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mariadb_innodb_status',
    source='mariadb',
    description='Retrieve InnoDB engine internals including deadlocks, buffer pool state, and I/O activity from SHOW ENGINE INNODB STATUS.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}, 'ssl': {'type': 'boolean'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'username', 'database', 'password'),
    requires=[],
    use_cases=[],
)
def get_mariadb_innodb_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MariaDBInnoDBStatusTool',
            attr='get_mariadb_innodb_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mariadb_innodb_status failed: {exc}"}
