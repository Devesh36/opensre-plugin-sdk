"""Bridged tool: list_gitlab_mrs (from OpenSRE app.tools.GitLabMRsTool)."""

from __future__ import annotations

from typing import Any

from gitlab_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_gitlab_mrs',
    source='gitlab',
    description='List recent merge requests for a GitLab project.',
    input_schema={'type': 'object', 'properties': {'project_id': {'type': 'string'}, 'target_branch': {'type': 'string', 'default': 'main'}, 'updated_after': {'type': 'string'}, 'per_page': {'type': 'integer', 'default': 10}, 'gitlab_url': {'type': 'string'}, 'gitlab_token': {'type': 'string'}}, 'required': ['project_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'access_token'),
    requires=['project_id'],
    use_cases=['Checking whether a recently merged MR introduced a failure', 'Correlating an incident window with recent code merges to the target branch', 'Identifying open MRs that may have deployed breaking changes'],
)
def list_gitlab_mrs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitLabMRsTool',
            attr='list_gitlab_mrs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_gitlab_mrs failed: {exc}"}
