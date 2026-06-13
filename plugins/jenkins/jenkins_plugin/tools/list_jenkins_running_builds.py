"""Bridged tool: list_jenkins_running_builds (from OpenSRE app.tools.JenkinsTool)."""

from __future__ import annotations

from typing import Any

from jenkins_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_jenkins_running_builds',
    source='jenkins',
    description='List Jenkins builds currently in progress across all jobs.',
    input_schema={'type': 'object', 'properties': {'jenkins_url': {'type': 'string'}, 'jenkins_user': {'type': 'string'}, 'jenkins_token': {'type': 'string'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'user', 'api_token'),
    requires=[],
    use_cases=['Checking whether a build is running right now during an active incident', 'Spotting a long-running or stuck build that may be causing impact'],
)
def list_jenkins_running_builds(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JenkinsTool',
            attr='list_jenkins_running_builds',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_jenkins_running_builds failed: {exc}"}
