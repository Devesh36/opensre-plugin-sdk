"""Bridged tool: get_jenkins_build_log (from OpenSRE app.tools.JenkinsTool)."""

from __future__ import annotations

from typing import Any

from jenkins_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_jenkins_build_log',
    source='jenkins',
    description='Fetch the console log for a specific Jenkins build.',
    input_schema={'type': 'object', 'properties': {'job_name': {'type': 'string'}, 'build_number': {'type': 'integer'}, 'jenkins_url': {'type': 'string'}, 'jenkins_user': {'type': 'string'}, 'jenkins_token': {'type': 'string'}}, 'required': ['job_name', 'build_number']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'user', 'api_token'),
    requires=['job_name', 'build_number'],
    use_cases=['Reading the error output of a failed build', 'Finding the stack trace or failing step that broke a deployment'],
)
def get_jenkins_build_log(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JenkinsTool',
            attr='get_jenkins_build_log',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_jenkins_build_log failed: {exc}"}
