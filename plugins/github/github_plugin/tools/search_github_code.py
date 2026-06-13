"""Bridged tool: search_github_code (from OpenSRE app.tools.GitHubSearchCodeTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='search_github_code',
    source='github',
    description='Search GitHub repository code through the configured GitHub MCP server.',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'query': {'type': 'string'}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo', 'query']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo', 'query'],
    use_cases=['Investigating alerts that mention a repository, branch, or commit', 'Finding source code related to failures, exceptions, and stack frames', 'Tracing config, workflow, or application code that may explain an incident'],
)
def search_github_code(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitHubSearchCodeTool',
            attr='search_github_code',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"search_github_code failed: {exc}"}
