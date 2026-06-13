"""Bridged tool: get_lambda_configuration (from OpenSRE app.tools.LambdaConfigTool)."""

from __future__ import annotations

from typing import Any

from cloudwatch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_lambda_configuration',
    source='cloudwatch',
    description='Get Lambda function configuration details (lightweight — no code retrieval).',
    input_schema={'type': 'object', 'properties': {'function_name': {'type': 'string'}}, 'required': ['function_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['function_name'],
    use_cases=['Quick configuration checks for Lambda functions', 'Environment variable inspection', 'Timeout and memory settings review'],
)
def get_lambda_configuration(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.LambdaConfigTool',
            attr='get_lambda_configuration',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_lambda_configuration failed: {exc}"}
