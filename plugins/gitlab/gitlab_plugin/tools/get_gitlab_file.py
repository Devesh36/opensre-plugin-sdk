"""Bridged tool: get_gitlab_file (from OpenSRE app.tools.GitLabFileTool)."""

from __future__ import annotations

from typing import Any

from gitlab_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_gitlab_file',
    source='gitlab',
    description='Read the contents of a specific file from a GitLab repository.',
    input_schema={'type': 'object', 'properties': {'project_id': {'type': 'string'}, 'file_path': {'type': 'string'}, 'ref': {'type': 'string', 'default': 'main'}, 'gitlab_url': {'type': 'string'}, 'gitlab_token': {'type': 'string'}}, 'required': ['project_id', 'file_path']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'access_token'),
    requires=['project_id', 'file_path'],
    use_cases=['Reading a config file that may explain a misconfiguration causing the incident', 'Inspecting a schema or manifest file referenced in the alert error message', 'Viewing a specific version of a file at the deployed commit or branch'],
)
def get_gitlab_file(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitLabFileTool',
            attr='get_gitlab_file_contents',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_gitlab_file failed: {exc}"}
