"""Bridged tool: get_postgresql_slow_queries (from OpenSRE app.tools.PostgreSQLSlowQueriesTool)."""

from __future__ import annotations

from typing import Any

from postgresql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_postgresql_slow_queries',
    source='postgresql',
    description='Retrieve slow PostgreSQL queries from pg_stat_statements extension, ranked by mean execution time.',
    input_schema={'properties': {'threshold_ms': {'default': 1000, 'description': 'Minimum mean execution time (ms) for query inclusion.', 'type': 'integer'}, 'port': {'default': 5432, 'description': 'PostgreSQL TCP port.', 'type': 'integer'}}, 'type': 'object', 'additionalProperties': False},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying slow queries that may be causing performance degradation', 'Analyzing query execution patterns during incident timeframes', 'Finding poorly optimized queries with high execution times or low cache hit rates'],
)
def get_postgresql_slow_queries(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.PostgreSQLSlowQueriesTool',
            attr='get_postgresql_slow_queries',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_postgresql_slow_queries failed: {exc}"}
