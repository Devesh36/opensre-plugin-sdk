"""Bridged tool: get_azure_sql_resource_stats (from OpenSRE app.tools.AzureSQLResourceStatsTool)."""

from __future__ import annotations

from typing import Any

from azure_sql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_azure_sql_resource_stats',
    source='azure_sql',
    description='Retrieve Azure SQL Database resource utilization history (CPU, IO, log throughput, memory) with throttling risk assessment.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}, 'minutes': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('server', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Diagnosing DTU/vCore throttling on Azure SQL Database', 'Identifying resource saturation causing query timeouts', 'Reviewing historical resource trends to determine if tier upgrade is needed'],
)
def get_azure_sql_resource_stats(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AzureSQLResourceStatsTool',
            attr='get_azure_sql_resource_stats',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_azure_sql_resource_stats failed: {exc}"}
