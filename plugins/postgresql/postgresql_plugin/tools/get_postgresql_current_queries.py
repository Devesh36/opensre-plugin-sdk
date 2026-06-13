"""Bridged tool: get_postgresql_current_queries (from OpenSRE app.tools.PostgreSQLCurrentQueriesTool)."""

from __future__ import annotations

from typing import Any

from postgresql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_postgresql_current_queries',
    source='postgresql',
    description='Retrieve currently executing PostgreSQL queries above a specific duration threshold.',
    input_schema={'type': 'object', 'properties': {'threshold_seconds': {'type': 'integer'}, 'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying long-running queries that may be causing performance issues', 'Investigating database locks and blocking queries during incidents', 'Finding resource-intensive queries correlating with alert timeframes'],
)
def get_postgresql_current_queries(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.PostgreSQLCurrentQueriesTool',
            attr='get_postgresql_current_queries',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_postgresql_current_queries failed: {exc}"}
