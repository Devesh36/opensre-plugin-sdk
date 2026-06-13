"""Bridged tool: jira_create_issue (from OpenSRE app.tools.JiraCreateIssueTool)."""

from __future__ import annotations

from typing import Any

from jira_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='jira_create_issue',
    source='jira',
    description='Create a new Jira issue to file an incident ticket with investigation findings, including summary, description, priority, and labels.',
    input_schema={'type': 'object', 'properties': {'summary': {'type': 'string', 'description': 'Issue title/summary'}, 'description': {'type': 'string', 'description': 'Issue description with investigation findings'}, 'issue_type': {'type': 'string', 'default': 'Bug', 'description': 'Jira issue type (e.g. Bug, Task, Incident)'}, 'priority': {'type': 'string', 'default': 'High', 'description': 'Issue priority (e.g. Highest, High, Medium, Low, Lowest)'}, 'labels': {'type': 'array', 'items': {'type': 'string'}, 'default': [], 'description': 'Labels to attach to the issue'}}, 'required': ['summary', 'description']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'email', 'api_token', 'project_key'),
    requires=['base_url', 'email', 'api_token', 'summary', 'description'],
    use_cases=['Filing a new incident ticket after root cause analysis', 'Creating a bug report from investigation findings', 'Tracking a production issue discovered during alert investigation', 'Documenting a new issue with evidence from the investigation'],
)
def jira_create_issue(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JiraCreateIssueTool',
            attr='jira_create_issue',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"jira_create_issue failed: {exc}"}
