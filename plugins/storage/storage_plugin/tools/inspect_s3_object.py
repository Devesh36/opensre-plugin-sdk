"""Bridged tool: inspect_s3_object (from OpenSRE app.tools.S3InspectTool)."""

from __future__ import annotations

from typing import Any

from storage_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='inspect_s3_object',
    source='storage',
    description="Inspect an S3 object's metadata and sample content.",
    input_schema={'type': 'object', 'properties': {'bucket': {'type': 'string'}, 'key': {'type': 'string'}}, 'required': ['bucket', 'key']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['bucket', 'key'],
    use_cases=['Tracing data lineage upstream to find root cause', 'Identifying schema changes in input data', 'Finding audit trails for external vendor interactions', 'Discovering which Lambda function produced the data'],
)
def inspect_s3_object(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.S3InspectTool',
            attr='inspect_s3_object',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"inspect_s3_object failed: {exc}"}
