"""Bridged tool: get_failed_jobs (from OpenSRE app.tools.TracerFailedJobsTool)."""

from __future__ import annotations

from typing import Any

from batch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_failed_jobs',
    source='batch',
    description='Get AWS Batch jobs that failed during a pipeline run.',
    input_schema={'type': 'object', 'properties': {'trace_id': {'type': 'string', 'description': 'The trace/run identifier'}}, 'required': ['trace_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('jwt_token',),
    requires=['trace_id'],
    use_cases=['Proving job failure hypothesis', 'Understanding container-level failures', 'Identifying infrastructure issues'],
)
def get_failed_jobs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerFailedJobsTool',
            attr='get_failed_jobs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_failed_jobs failed: {exc}"}
