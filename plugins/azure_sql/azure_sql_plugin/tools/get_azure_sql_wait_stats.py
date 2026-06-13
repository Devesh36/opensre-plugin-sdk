"""Bridged tool: get_azure_sql_wait_stats (from OpenSRE app.tools.AzureSQLWaitStatsTool)."""

from __future__ import annotations

from typing import Any

from azure_sql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_azure_sql_wait_stats',
    source='azure_sql',
    description='Retrieve top wait statistics from Azure SQL Database to diagnose throttling, lock contention, IO bottlenecks, and network issues.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('server', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Identifying the most impactful wait types during an incident', 'Diagnosing lock contention or IO bottlenecks', 'Understanding resource governance limits on Azure SQL'],
)
def get_azure_sql_wait_stats(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AzureSQLWaitStatsTool',
            attr='get_azure_sql_wait_stats',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_azure_sql_wait_stats failed: {exc}"}
