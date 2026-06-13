"""Bridged tool: get_lambda_invocation_logs (from OpenSRE app.tools.LambdaInvocationLogsTool)."""

from __future__ import annotations

from typing import Any

from cloudwatch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_lambda_invocation_logs',
    source='cloudwatch',
    description='Get Lambda invocation logs from CloudWatch.',
    input_schema={'type': 'object', 'properties': {'function_name': {'type': 'string'}, 'request_id': {'type': 'string'}, 'filter_errors': {'type': 'boolean', 'default': False}, 'limit': {'type': 'integer', 'default': 50}}, 'required': ['function_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['function_name'],
    use_cases=['Finding error messages and stack traces from Lambda executions', 'Understanding data processing flow in Lambda functions', 'Identifying issues with external API calls made by Lambda', 'Tracing data transformation logic through log output'],
)
def get_lambda_invocation_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.LambdaInvocationLogsTool',
            attr='get_lambda_invocation_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_lambda_invocation_logs failed: {exc}"}
