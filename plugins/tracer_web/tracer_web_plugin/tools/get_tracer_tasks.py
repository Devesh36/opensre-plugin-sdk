"""Bridged tool: get_tracer_tasks (from OpenSRE app.tools.TracerTasksTool)."""

from __future__ import annotations

from typing import Any

from tracer_web_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_tracer_tasks',
    source='tracer_web',
    description='Get tasks for a specific pipeline run from the Tracer API.',
    input_schema={'type': 'object', 'properties': {'run_id': {'type': 'string', 'description': 'The unique identifier for the pipeline run'}}, 'required': ['run_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('jwt_token', 'api_url'),
    requires=['run_id'],
    use_cases=['Retrieving detailed task information for a pipeline run', 'Understanding which specific tasks failed or succeeded'],
)
def get_tracer_tasks(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerTasksTool',
            attr='get_tracer_tasks',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_tracer_tasks failed: {exc}"}
