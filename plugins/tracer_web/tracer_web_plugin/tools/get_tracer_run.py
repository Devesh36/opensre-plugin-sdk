"""Bridged tool: get_tracer_run (from OpenSRE app.tools.TracerRunTool)."""

from __future__ import annotations

from typing import Any

from tracer_web_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_tracer_run',
    source='tracer_web',
    description='Get the latest pipeline run from the Tracer API.',
    input_schema={'type': 'object', 'properties': {'pipeline_name': {'type': 'string'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('jwt_token', 'api_url'),
    requires=[],
    use_cases=['Retrieving the most recent run information for a Tracer pipeline', 'Checking current pipeline run status and metadata'],
)
def get_tracer_run(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerRunTool',
            attr='get_tracer_run',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_tracer_run failed: {exc}"}
