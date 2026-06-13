"""Bridged tool: list_s3_objects (from OpenSRE app.tools.S3ListTool)."""

from __future__ import annotations

from typing import Any

from storage_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_s3_objects',
    source='storage',
    description='List objects in an S3 bucket with optional prefix filter.',
    input_schema={'type': 'object', 'properties': {'bucket': {'type': 'string'}, 'prefix': {'type': 'string', 'default': ''}, 'max_keys': {'type': 'integer', 'default': 100}}, 'required': ['bucket']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['bucket'],
    use_cases=['Exploring S3 bucket contents and finding relevant data files', 'Verifying which files are present in a pipeline output location'],
)
def list_s3_objects(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.S3ListTool',
            attr='list_s3_objects',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_s3_objects failed: {exc}"}
