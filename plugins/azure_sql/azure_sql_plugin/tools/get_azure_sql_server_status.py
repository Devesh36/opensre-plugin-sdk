"""Bridged tool: get_azure_sql_server_status (from OpenSRE app.tools.AzureSQLServerStatusTool)."""

from __future__ import annotations

from typing import Any

from azure_sql_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_azure_sql_server_status',
    source='azure_sql',
    description='Retrieve Azure SQL Database server metrics including service tier, resource utilization, connections, and database size.',
    input_schema={'type': 'object', 'properties': {'port': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('server', 'database', 'username', 'password'),
    requires=[],
    use_cases=['Checking Azure SQL Database health during an incident', 'Identifying DTU/vCore throttling or resource exhaustion', 'Reviewing service tier and connection saturation'],
)
def get_azure_sql_server_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AzureSQLServerStatusTool',
            attr='get_azure_sql_server_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_azure_sql_server_status failed: {exc}"}
