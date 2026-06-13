"""Bridged tool: get_lambda_errors (from OpenSRE app.tools.LambdaErrorsTool)."""

from __future__ import annotations

from typing import Any

from cloudwatch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_lambda_errors',
    source='cloudwatch',
    description='Get Lambda function error logs.',
    input_schema={'type': 'object', 'properties': {'function_name': {'type': 'string'}, 'limit': {'type': 'integer', 'default': 50}}, 'required': ['function_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['function_name'],
    use_cases=['Quickly finding error messages from a Lambda function', 'Understanding Lambda failure patterns', 'Identifying root cause of Lambda failures'],
)
def get_lambda_errors(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.LambdaErrorsTool',
            attr='get_lambda_errors',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_lambda_errors failed: {exc}"}
