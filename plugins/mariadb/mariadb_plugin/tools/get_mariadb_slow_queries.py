"""Bridged tool: get_mariadb_slow_queries (from OpenSRE app.tools.MariaDBSlowQueriesTool)."""

from __future__ import annotations

from typing import Any

from mariadb_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mariadb_slow_queries',
    source='mariadb',
    description='Retrieve top MariaDB queries by average execution time from performance_schema.events_statements_summary_by_digest.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}, 'ssl': {'type': 'boolean'}, 'max_results': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'username', 'database', 'password'),
    requires=[],
    use_cases=[],
)
def get_mariadb_slow_queries(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MariaDBSlowQueriesTool',
            attr='get_mariadb_slow_queries',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mariadb_slow_queries failed: {exc}"}
