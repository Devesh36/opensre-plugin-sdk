"""Bridged tool: get_mongodb_server_status (from OpenSRE app.tools.MongoDBServerStatusTool)."""

from __future__ import annotations

from typing import Any

from mongodb_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mongodb_server_status',
    source='mongodb',
    description='Retrieve high-level MongoDB server status including connections, memory usage, and operation counters.',
    input_schema={'type': 'object', 'properties': {'auth_source': {'type': 'string'}, 'tls': {'type': 'boolean'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('connection_string', 'database'),
    requires=[],
    use_cases=[],
)
def get_mongodb_server_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MongoDBServerStatusTool',
            attr='get_mongodb_server_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mongodb_server_status failed: {exc}"}
