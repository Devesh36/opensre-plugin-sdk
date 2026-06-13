"""Bridged tool: get_cloudwatch_logs (from OpenSRE app.tools.CloudWatchLogsTool)."""

from __future__ import annotations

from typing import Any

from cloudwatch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_cloudwatch_logs',
    source='cloudwatch',
    description='Fetch error logs from AWS CloudWatch Logs.',
    input_schema={'type': 'object', 'properties': {'log_group': {'type': 'string', 'description': 'CloudWatch log group name (required)'}, 'log_stream': {'type': 'string', 'description': 'Log stream name (optional — auto-discovered if absent)'}, 'filter_pattern': {'type': 'string', 'description': 'Pattern to filter logs (e.g., correlation_id, error text)'}, 'limit': {'type': 'integer', 'default': 100}}, 'required': ['log_group']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=[],
    use_cases=['Retrieving error tracebacks from CloudWatch', 'Analyzing application-level errors', 'Investigating file not found errors', 'Understanding pipeline failure root causes', 'Auto-discovering recent logs from ECS tasks, Lambda functions, etc.', 'Searching for logs by correlation ID or error pattern'],
)
def get_cloudwatch_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.CloudWatchLogsTool',
            attr='get_cloudwatch_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_cloudwatch_logs failed: {exc}"}
