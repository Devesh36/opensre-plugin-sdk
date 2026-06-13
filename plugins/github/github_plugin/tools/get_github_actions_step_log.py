"""Bridged tool: get_github_actions_step_log (from OpenSRE app.tools.GitHubActionsTool)."""

from __future__ import annotations

from typing import Any

from github_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_github_actions_step_log',
    source='github',
    description='Fetch the log output for a failed GitHub Actions job step.',
    input_schema={'type': 'object', 'properties': {'owner': {'type': 'string'}, 'repo': {'type': 'string'}, 'run_id': {'type': 'integer'}, 'job_id': {'type': 'integer'}, 'step_name': {'type': 'string', 'default': ''}, 'step_number': {'type': 'integer'}, 'tail_lines': {'type': 'integer', 'default': 500}, 'github_url': {'type': 'string'}, 'github_mode': {'type': 'string'}, 'github_token': {'type': 'string'}}, 'required': ['owner', 'repo', 'run_id', 'job_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('auth_token',),
    requires=['owner', 'repo', 'run_id', 'job_id'],
    use_cases=['Reading the error output for the step that broke a deployment', 'Checking the exact log snippet for a flaky test or secret-related failure'],
)
def get_github_actions_step_log(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GitHubActionsTool',
            attr='get_github_actions_step_log',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_github_actions_step_log failed: {exc}"}
