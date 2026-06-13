"""Bridged tool: jira_search_issues (from OpenSRE app.tools.JiraSearchIssuesTool)."""

from __future__ import annotations

from typing import Any

from jira_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='jira_search_issues',
    source='jira',
    description='Search Jira issues using JQL to find related incidents, open bugs, or recent tasks that may provide context for the current investigation.',
    input_schema={'type': 'object', 'properties': {'jql': {'type': 'string', 'default': '', 'description': 'JQL query string (e.g. status = Open AND priority = High)'}, 'max_results': {'type': 'integer', 'default': 20, 'description': 'Maximum number of issues to return'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'email', 'api_token', 'project_key'),
    requires=['base_url', 'email', 'api_token'],
    use_cases=['Finding open bugs or incidents for a specific service or component', 'Searching for recent Jira issues related to the alert under investigation', 'Checking whether a similar incident was already filed in Jira', 'Listing high-priority issues updated recently in a project'],
)
def jira_search_issues(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JiraSearchIssuesTool',
            attr='jira_search_issues',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"jira_search_issues failed: {exc}"}
