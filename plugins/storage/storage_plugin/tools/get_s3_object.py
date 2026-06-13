"""Bridged tool: get_s3_object (from OpenSRE app.tools.S3GetObjectTool)."""

from __future__ import annotations

from typing import Any

from storage_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_s3_object',
    source='storage',
    description='Get full S3 object content — audit payloads, configs, lineage data.',
    input_schema={'type': 'object', 'properties': {'bucket': {'type': 'string'}, 'key': {'type': 'string'}}, 'required': ['bucket', 'key']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['bucket', 'key'],
    use_cases=['Retrieving audit payloads when audit_key found in S3 metadata', 'Tracing external vendor interactions that caused failures', 'Reading configuration or manifest files', 'Finding upstream data lineage details'],
)
def get_s3_object(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.S3GetObjectTool',
            attr='get_s3_object',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_s3_object failed: {exc}"}
