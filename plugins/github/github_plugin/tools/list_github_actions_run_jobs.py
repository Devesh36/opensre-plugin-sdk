"""Bridged tool: list_github_actions_run_jobs (from OpenSRE app.tools.GitHubActionsTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_github_actions_run_jobs',
    source='github',
    description='List jobs and step outcomes for a GitHub Actions workflow run.',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'run_id': {'type': 'integer'}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo', 'run_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo', 'run_id'],
    use_cases=['Finding which job failed in a deployment workflow', 'Checking step-by-step status for test, build, and deploy jobs'],
)
def list_github_actions_run_jobs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitHubActionsTool',
            attr='list_github_actions_run_jobs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_github_actions_run_jobs failed: {exc}"}
