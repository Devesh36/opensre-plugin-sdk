"""Bridged tool: list_gitlab_commits (from OpenSRE app.tools.GitLabCommitsTool)."""

from __future__ import annotations

from typing import Any

from gitlab_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_gitlab_commits',
    source='gitlab',
    description='List recent commits for a gitlab repository.',
    input_schema={'type': 'object', 'properties': {'project_id': {'type': 'string'}, 'ref_name': {'type': 'string', 'default': ''}, 'since': {'type': 'string'}, 'per_page': {'type': 'integer', 'default': 10}, 'gitlab_url': {'type': 'string'}, 'gitlab_token': {'type': 'string'}}, 'required': ['project_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'access_token'),
    requires=['project_id'],
    use_cases=['Checking whether a recent change could explain a failure', 'Correlating a deployment or incident window with code changes'],
)
def list_gitlab_commits(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitLabCommitsTool',
            attr='list_gitlab_commits',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_gitlab_commits failed: {exc}"}
