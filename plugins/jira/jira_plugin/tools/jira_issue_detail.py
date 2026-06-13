"""Bridged tool: jira_issue_detail (from OpenSRE app.tools.JiraIssueDetailTool)."""

from __future__ import annotations

from typing import Any

from jira_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='jira_issue_detail',
    source='jira',
    description='Fetch the full details of a specific Jira issue to pull context, status, and description into the current investigation.',
    input_schema={'type': 'object', 'properties': {'issue_key': {'type': 'string', 'description': 'Jira issue key to fetch (e.g. OPS-123)'}}, 'required': ['issue_key']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'email', 'api_token', 'project_key'),
    requires=['base_url', 'email', 'api_token', 'issue_key'],
    use_cases=['Getting the full description and context of a Jira incident ticket', 'Checking the current status and priority of a known issue', 'Reading issue details to correlate with alert findings', 'Pulling assignee and label information for an existing ticket'],
)
def jira_issue_detail(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JiraIssueDetailTool',
            attr='jira_issue_detail',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"jira_issue_detail failed: {exc}"}
