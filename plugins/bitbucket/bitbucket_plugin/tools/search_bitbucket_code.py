"""Bridged tool: search_bitbucket_code (from OpenSRE app.tools.BitbucketSearchCodeTool)."""

from __future__ import annotations

from typing import Any

from bitbucket_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='search_bitbucket_code',
    source='bitbucket',
    description='Search code across a Bitbucket workspace or specific repository.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string'}, 'repo_slug': {'type': 'string', 'default': ''}, 'limit': {'type': 'integer', 'default': 20}, 'max_results': {'type': 'integer'}, 'integration_id': {'type': 'string'}}, 'required': ['query']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('workspace', 'username', 'app_password', 'base_url'),
    requires=['query'],
    use_cases=['Finding where a specific function or configuration is defined', 'Searching for error patterns across repositories'],
)
def search_bitbucket_code(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.BitbucketSearchCodeTool',
            attr='search_bitbucket_code',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"search_bitbucket_code failed: {exc}"}
