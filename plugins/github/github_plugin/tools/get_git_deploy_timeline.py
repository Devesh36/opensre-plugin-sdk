"""Bridged tool: get_git_deploy_timeline (from OpenSRE app.tools.GitDeployTimelineTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_git_deploy_timeline',
    source='github',
    description='List commits on a GitHub branch within a time window (defaults to the last 120 minutes). Used to correlate an alert with recent deploys by asking "what changed right before this fired?"',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'branch': {'type': 'string', 'default': 'main'}, 'since': {'type': 'string', 'description': 'ISO-8601 window start (e.g. 2026-04-20T10:00:00Z). Optional.'}, 'until': {'type': 'string', 'description': 'ISO-8601 window end. Defaults to now.'}, 'window_minutes_before_alert': {'type': 'integer', 'description': "Convenience: minutes back from 'until' (or now) when 'since' is omitted. Clamped to 10080 minutes. When omitted, the tool prefers the shared incident window from state if one is available, otherwise falls back to 120 minutes."}, 'per_page': {'type': 'integer', 'default': 30, 'minimum': 1, 'maximum': 100}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo'],
    use_cases=['Correlating an incident with recent code changes on the default branch', 'Checking whether a deploy landed within the alert window', 'Building a short-form deploy timeline for RCA narrative'],
)
def get_git_deploy_timeline(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitDeployTimelineTool',
            attr='get_git_deploy_timeline',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_git_deploy_timeline failed: {exc}"}
