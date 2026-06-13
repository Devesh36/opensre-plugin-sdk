"""Bridged tool: query_opensearch_analytics (from OpenSRE app.tools.OpenSearchAnalyticsTool)."""

from __future__ import annotations

from typing import Any

from opensearch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_opensearch_analytics',
    source='opensearch',
    description='Query OpenSearch-compatible analytics indices with bounded retrieval.',
    input_schema={'type': 'object', 'properties': {'index_pattern': {'type': 'string', 'default': '*'}, 'query': {'type': 'string', 'default': '*'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 50}, 'max_results': {'type': 'integer', 'default': 100}, 'integration_id': {'type': 'string'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key', 'username', 'password'),
    requires=['url'],
    use_cases=[],
)
def query_opensearch_analytics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpenSearchAnalyticsTool',
            attr='query_opensearch_analytics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_opensearch_analytics failed: {exc}"}
