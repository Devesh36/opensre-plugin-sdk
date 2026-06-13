"""Bridged tool: query_snowflake_history (from OpenSRE app.tools.SnowflakeQueryHistoryTool)."""

from __future__ import annotations

from typing import Any

from snowflake_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_snowflake_history',
    source='snowflake',
    description='Query Snowflake query history using a read-only bounded statement.',
    input_schema={'type': 'object', 'properties': {'account_identifier': {'type': 'string'}, 'query': {'type': 'string'}, 'limit': {'type': 'integer', 'default': 50}, 'max_results': {'type': 'integer', 'default': 50}, 'user': {'type': 'string'}, 'warehouse': {'type': 'string'}, 'role': {'type': 'string'}, 'database': {'type': 'string'}, 'db_schema': {'type': 'string'}, 'integration_id': {'type': 'string'}, 'timeout_seconds': {'type': 'number', 'default': 20.0}}, 'required': ['account_identifier']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('password', 'token', 'account'),
    requires=['account_identifier'],
    use_cases=[],
)
def query_snowflake_history(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SnowflakeQueryHistoryTool',
            attr='query_snowflake_history',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_snowflake_history failed: {exc}"}
