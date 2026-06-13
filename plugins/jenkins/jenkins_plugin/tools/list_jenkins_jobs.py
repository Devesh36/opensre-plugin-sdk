"""Bridged tool: list_jenkins_jobs (from OpenSRE app.tools.JenkinsTool)."""

from __future__ import annotations

from typing import Any

from jenkins_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_jenkins_jobs',
    source='jenkins',
    description='List Jenkins jobs with their last-build status.',
    input_schema={'type': 'object', 'properties': {'jenkins_url': {'type': 'string'}, 'jenkins_user': {'type': 'string'}, 'jenkins_token': {'type': 'string'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'user', 'api_token'),
    requires=[],
    use_cases=['Discovering which jobs exist when the failing job name is unknown', 'Getting an overview of which pipelines are passing or failing'],
)
def list_jenkins_jobs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JenkinsTool',
            attr='list_jenkins_jobs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_jenkins_jobs failed: {exc}"}
