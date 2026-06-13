"""Bridged tool: list_github_actions_workflow_runs (from OpenSRE app.tools.GitHubActionsTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_github_actions_workflow_runs',
    source='github',
    description='List recent GitHub Actions workflow runs for a repository.',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'branch': {'type': 'string', 'default': ''}, 'status': {'type': 'string', 'default': ''}, 'event': {'type': 'string', 'default': ''}, 'per_page': {'type': 'integer', 'default': 30}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo'],
    use_cases=['Checking which deploy or test workflow failed right before an incident', 'Reviewing recent workflow status, trigger, and branch context', 'Finding a run that matches an outage window or rollback event'],
)
def list_github_actions_workflow_runs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitHubActionsTool',
            attr='list_github_actions_workflow_runs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_github_actions_workflow_runs failed: {exc}"}
