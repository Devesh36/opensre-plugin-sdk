"""Bridged tool: get_github_repository_tree (from OpenSRE app.tools.GitHubRepositoryTreeTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_github_repository_tree',
    source='github',
    description='Browse a GitHub repository tree through the MCP server.',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'path_filter': {'type': 'string', 'default': ''}, 'recursive': {'type': 'boolean', 'default': True}, 'tree_sha': {'type': 'string', 'default': ''}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo'],
    use_cases=['Understanding repository structure during an incident', 'Finding likely directories for runtime code, configs, or workflows', 'Narrowing down where to read code next'],
)
def get_github_repository_tree(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitHubRepositoryTreeTool',
            attr='get_github_repository_tree',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_github_repository_tree failed: {exc}"}
