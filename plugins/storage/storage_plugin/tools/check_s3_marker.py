"""Bridged tool: check_s3_marker (from OpenSRE app.tools.S3MarkerTool)."""

from __future__ import annotations

from typing import Any

from storage_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='check_s3_marker',
    source='storage',
    description='Check if a _SUCCESS marker exists in S3 storage to verify pipeline completion.',
    input_schema={'type': 'object', 'properties': {'bucket': {'type': 'string'}, 'prefix': {'type': 'string'}}, 'required': ['bucket', 'prefix']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=[],
    use_cases=['Verifying if a data pipeline run completed successfully', 'Checking for presence of a _SUCCESS marker file'],
)
def check_s3_marker(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.S3MarkerTool',
            attr='check_s3_marker',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"check_s3_marker failed: {exc}"}
