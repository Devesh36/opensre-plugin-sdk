"""Bridged tool: query_elasticsearch_logs (from OpenSRE app.tools.ElasticsearchLogsTool)."""

from __future__ import annotations

from typing import Any

from elasticsearch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_elasticsearch_logs',
    source='elasticsearch',
    description='Search Elasticsearch logs for errors, exceptions, and application events.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'Lucene/KQL query string (default: *)'}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 50}, 'index_pattern': {'type': 'string', 'description': "Index pattern to search (e.g. 'logs-*'). Defaults to ELASTICSEARCH_INDEX_PATTERN env var or '*'."}}, 'required': ['query']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key', 'username', 'password'),
    requires=[],
    use_cases=['Investigating application errors stored in Elasticsearch', 'Searching logs across multiple indices or data streams', 'Filtering logs by time range and query string', 'Inspecting cluster health and available indices'],
)
def query_elasticsearch_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.ElasticsearchLogsTool',
            attr='query_elasticsearch_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_elasticsearch_logs failed: {exc}"}
