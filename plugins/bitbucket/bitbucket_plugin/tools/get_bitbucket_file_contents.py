"""Bridged tool: get_bitbucket_file_contents (from OpenSRE app.tools.BitbucketFileContentsTool)."""

from __future__ import annotations

from typing import Any

from bitbucket_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_bitbucket_file_contents',
    source='bitbucket',
    description='Retrieve the contents of a file from a Bitbucket repository at a specific revision.',
    input_schema={'type': 'object', 'properties': {'repo_slug': {'type': 'string'}, 'path': {'type': 'string'}, 'ref': {'type': 'string', 'default': ''}, 'max_results': {'type': 'integer'}, 'integration_id': {'type': 'string'}}, 'required': ['repo_slug', 'path']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('workspace', 'username', 'app_password', 'base_url'),
    requires=['repo_slug', 'path'],
    use_cases=['Reading configuration files that may explain a failure', 'Comparing file contents between revisions during investigation'],
)
def get_bitbucket_file_contents(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.BitbucketFileContentsTool',
            attr='get_bitbucket_file_contents',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_bitbucket_file_contents failed: {exc}"}
