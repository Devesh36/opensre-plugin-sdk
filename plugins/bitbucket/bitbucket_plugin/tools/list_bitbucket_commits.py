"""Bridged tool: list_bitbucket_commits (from OpenSRE app.tools.BitbucketCommitsTool)."""

from __future__ import annotations

from typing import Any

from bitbucket_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_bitbucket_commits',
    source='bitbucket',
    description='List recent commits for a Bitbucket repository, optionally filtered by file path.',
    input_schema={'type': 'object', 'properties': {'repo_slug': {'type': 'string'}, 'path': {'type': 'string', 'default': ''}, 'limit': {'type': 'integer', 'default': 20}, 'max_results': {'type': 'integer'}, 'integration_id': {'type': 'string'}}, 'required': ['repo_slug']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('workspace', 'username', 'app_password', 'base_url'),
    requires=['repo_slug'],
    use_cases=['Checking whether a recent change could explain a failure', 'Reviewing commit history for a specific file or directory'],
)
def list_bitbucket_commits(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.BitbucketCommitsTool',
            attr='list_bitbucket_commits',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_bitbucket_commits failed: {exc}"}
