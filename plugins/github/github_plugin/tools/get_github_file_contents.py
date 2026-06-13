"""Bridged tool: get_github_file_contents (from OpenSRE app.tools.GitHubFileContentsTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_github_file_contents',
    source='github',
    description='Fetch a file or directory from GitHub through the MCP server.',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'path': {'type': 'string'}, 'ref': {'type': 'string', 'default': ''}, 'sha': {'type': 'string', 'default': ''}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo', 'path']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo', 'path'],
    use_cases=['Reading application code referenced by an alert', 'Inspecting CI config, manifests, and deployment files', 'Checking how a specific path looked on a branch or commit'],
)
def get_github_file_contents(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitHubFileContentsTool',
            attr='get_github_file_contents',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_github_file_contents failed: {exc}"}
