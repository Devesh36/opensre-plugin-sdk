"""Bridged tool: list_github_commits (from OpenSRE app.tools.GitHubCommitsTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_github_commits',
    source='github',
    description='List recent commits for a GitHub repository through the MCP server.',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'path': {'type': 'string', 'default': ''}, 'sha': {'type': 'string', 'default': ''}, 'per_page': {'type': 'integer', 'default': 10}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo'],
    use_cases=['Checking whether a recent change could explain a failure', 'Reviewing commit history for a specific file or directory', 'Correlating a deployment or incident window with code changes'],
)
def list_github_commits(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitHubCommitsTool',
            attr='list_github_commits',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_github_commits failed: {exc}"}
