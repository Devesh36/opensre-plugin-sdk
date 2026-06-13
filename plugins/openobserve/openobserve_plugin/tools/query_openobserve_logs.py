"""Bridged tool: query_openobserve_logs (from OpenSRE app.tools.OpenObserveLogsTool)."""

from __future__ import annotations

from typing import Any

from openobserve_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_openobserve_logs',
    source='openobserve',
    description='Query OpenObserve logs using bounded read-only search.',
    input_schema={'type': 'object', 'properties': {'base_url': {'type': 'string'}, 'org': {'type': 'string', 'default': 'default'}, 'stream': {'type': 'string', 'default': ''}, 'query': {'type': 'string'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 50}, 'max_results': {'type': 'integer', 'default': 100}, 'integration_id': {'type': 'string'}, 'timeout_seconds': {'type': 'number', 'default': 20.0}}, 'required': ['base_url']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_token', 'username', 'password', 'url', 'token'),
    requires=['base_url'],
    use_cases=[],
)
def query_openobserve_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpenObserveLogsTool',
            attr='query_openobserve_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_openobserve_logs failed: {exc}"}
