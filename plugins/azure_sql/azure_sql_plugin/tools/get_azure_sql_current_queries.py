"""Bridged tool: get_azure_sql_current_queries (from OpenSRE app.tools.AzureSQLCurrentQueriesTool)."""

from __future__ import annotations

from typing import Any

from azure_sql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_azure_sql_current_queries',
    source='azure_sql',
    description='Retrieve currently running queries on Azure SQL Database above a duration threshold, including wait types and resource usage.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}, 'threshold_seconds': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('server', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying long-running queries causing lock contention', 'Diagnosing blocking chains during an Azure SQL incident', 'Finding queries consuming excessive CPU or IO'],
)
def get_azure_sql_current_queries(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AzureSQLCurrentQueriesTool',
            attr='get_azure_sql_current_queries',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_azure_sql_current_queries failed: {exc}"}
