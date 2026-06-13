"""Bridged tool: get_mysql_current_processes (from OpenSRE app.tools.MySQLCurrentProcessesTool)."""

from __future__ import annotations

from typing import Any

from mysql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mysql_current_processes',
    source='mysql',
    description='Retrieve currently active MySQL processes above a duration threshold, excluding sleeping connections.',
    input_schema={'type': 'object', 'properties': {'threshold_seconds': {'type': 'integer'}, 'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying long-running queries blocking other operations', 'Investigating lock contention or deadlock situations', 'Spotting runaway queries during an incident'],
)
def get_mysql_current_processes(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MySQLCurrentProcessesTool',
            attr='get_mysql_current_processes',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mysql_current_processes failed: {exc}"}
