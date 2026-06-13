"""Bridged tool: inspect_lambda_function (from OpenSRE app.tools.LambdaInspectTool)."""

from __future__ import annotations

from typing import Any

from cloudwatch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='inspect_lambda_function',
    source='cloudwatch',
    description="Inspect a Lambda function's configuration and optionally its code.",
    input_schema={'type': 'object', 'properties': {'function_name': {'type': 'string'}, 'include_code': {'type': 'boolean', 'default': True}}, 'required': ['function_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['function_name'],
    use_cases=['Understanding function configuration (timeout, memory, env vars)', 'Reviewing function code for data transformation logic', 'Identifying environment-related issues', 'Finding integration points with other services'],
)
def inspect_lambda_function(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.LambdaInspectTool',
            attr='inspect_lambda_function',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"inspect_lambda_function failed: {exc}"}
