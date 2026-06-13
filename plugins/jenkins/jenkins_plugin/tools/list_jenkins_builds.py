"""Bridged tool: list_jenkins_builds (from OpenSRE app.tools.JenkinsTool)."""

from __future__ import annotations

from typing import Any

from jenkins_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_jenkins_builds',
    source='jenkins',
    description='List recent Jenkins builds for a job with status and timestamp.',
    input_schema={'type': 'object', 'properties': {'job_name': {'type': 'string'}, 'limit': {'type': 'integer', 'default': 10}, 'status': {'type': 'string', 'default': '', 'description': 'Optional filter: SUCCESS, FAILURE, RUNNING, ABORTED'}, 'jenkins_url': {'type': 'string'}, 'jenkins_user': {'type': 'string'}, 'jenkins_token': {'type': 'string'}}, 'required': ['job_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'user', 'api_token'),
    requires=['job_name'],
    use_cases=['Checking whether a recent build or deployment coincided with the alert', 'Identifying which build failed and when', 'Correlating a deployment window with downstream errors in logs or metrics'],
)
def list_jenkins_builds(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JenkinsTool',
            attr='list_jenkins_builds',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_jenkins_builds failed: {exc}"}
