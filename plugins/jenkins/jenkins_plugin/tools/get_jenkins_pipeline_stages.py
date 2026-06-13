"""Bridged tool: get_jenkins_pipeline_stages (from OpenSRE app.tools.JenkinsTool)."""

from __future__ import annotations

from typing import Any

from jenkins_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_jenkins_pipeline_stages',
    source='jenkins',
    description='List the pipeline stages of a Jenkins build with per-stage status and duration.',
    input_schema={'type': 'object', 'properties': {'job_name': {'type': 'string'}, 'build_number': {'type': 'integer'}, 'jenkins_url': {'type': 'string'}, 'jenkins_user': {'type': 'string'}, 'jenkins_token': {'type': 'string'}}, 'required': ['job_name', 'build_number']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'user', 'api_token'),
    requires=['job_name', 'build_number'],
    use_cases=['Identifying which pipeline stage failed in a deployment', 'Seeing how long each stage took to spot a slow or stuck stage'],
)
def get_jenkins_pipeline_stages(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JenkinsTool',
            attr='get_jenkins_pipeline_stages',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_jenkins_pipeline_stages failed: {exc}"}
