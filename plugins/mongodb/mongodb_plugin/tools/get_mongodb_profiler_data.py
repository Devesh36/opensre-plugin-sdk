"""Bridged tool: get_mongodb_profiler_data (from OpenSRE app.tools.MongoDBProfilerTool)."""

from __future__ import annotations

from typing import Any

from mongodb_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mongodb_profiler_data',
    source='mongodb',
    description='Retrieve slow queries from the MongoDB database system.profile collection (requires profiling enabled).',
    input_schema={'type': 'object', 'properties': {'threshold_ms': {'type': 'integer'}, 'auth_source': {'type': 'string'}, 'tls': {'type': 'boolean'}, 'limit': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('connection_string', 'database'),
    requires=[],
    use_cases=[],
)
def get_mongodb_profiler_data(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MongoDBProfilerTool',
            attr='get_mongodb_profiler_data',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mongodb_profiler_data failed: {exc}"}
