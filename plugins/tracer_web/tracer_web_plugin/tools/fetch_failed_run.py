"""Bridged tool: fetch_failed_run (from OpenSRE app.tools.TracerFailedRunTool)."""

from __future__ import annotations

from typing import Any

from tracer_web_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='fetch_failed_run',
    source='tracer_web',
    description='Fetch context (metadata) about a failed run from the Tracer Web App.',
    input_schema={'type': 'object', 'properties': {'pipeline_name': {'type': 'string', 'description': 'Optional pipeline name to filter runs'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('jwt_token', 'api_url'),
    requires=[],
    use_cases=['Getting details of the most recent failed pipeline run', 'Finding the trace_id needed for deeper investigation'],
)
def fetch_failed_run(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerFailedRunTool',
            attr='fetch_failed_run',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"fetch_failed_run failed: {exc}"}
