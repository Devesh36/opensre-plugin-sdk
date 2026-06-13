"""Bridged tool: list_github_actions_active_runs (from OpenSRE app.tools.GitHubActionsTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_github_actions_active_runs',
    source='github',
    description='List GitHub Actions workflow runs that are currently queued or in progress.',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'per_page': {'type': 'integer', 'default': 30}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo'],
    use_cases=['Seeing what deployment jobs are still running during an incident', 'Spotting queued deploys that may be waiting on a shared runner or lock'],
)
def list_github_actions_active_runs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitHubActionsTool',
            attr='list_github_actions_active_runs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_github_actions_active_runs failed: {exc}"}
