"""Bridged tool: get_postgresql_replication_status (from OpenSRE app.tools.PostgreSQLReplicationStatusTool)."""

from __future__ import annotations

from typing import Any

from postgresql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_postgresql_replication_status',
    source='postgresql',
    description='Retrieve PostgreSQL replication status including replica lag, WAL positions, and streaming status.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Investigating replication lag issues during database incidents', 'Checking replica health and synchronization status', 'Monitoring WAL streaming and replica connectivity problems'],
)
def get_postgresql_replication_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.PostgreSQLReplicationStatusTool',
            attr='get_postgresql_replication_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_postgresql_replication_status failed: {exc}"}
