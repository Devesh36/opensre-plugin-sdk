"""Bridged tool: list_gitlab_pipelines (from OpenSRE app.tools.GitLabPipelinesTool)."""

from __future__ import annotations

from typing import Any

from gitlab_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_gitlab_pipelines',
    source='gitlab',
    description='List recent CI/CD pipelines for a GitLab project.',
    input_schema={'type': 'object', 'properties': {'project_id': {'type': 'string'}, 'ref': {'type': 'string', 'default': 'main'}, 'updated_after': {'type': 'string'}, 'status': {'type': 'string', 'default': 'failed'}, 'per_page': {'type': 'integer', 'default': 10}, 'gitlab_url': {'type': 'string'}, 'gitlab_token': {'type': 'string'}}, 'required': ['project_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'access_token'),
    requires=['project_id'],
    use_cases=['Checking whether a failed pipeline caused or coincided with the incident', 'Correlating a deployment window with a pipeline that ran around the alert time', 'Identifying which CI job failed and on which branch'],
)
def list_gitlab_pipelines(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitLabPipelinesTool',
            attr='list_gitlab_pipelines',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_gitlab_pipelines failed: {exc}"}
