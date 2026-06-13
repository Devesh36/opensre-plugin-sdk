"""Bridged tool: jira_add_comment (from OpenSRE app.tools.JiraAddCommentTool)."""

from __future__ import annotations

from typing import Any

from jira_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='jira_add_comment',
    source='jira',
    description='Post investigation findings, root cause analysis, or status updates as a comment on an existing Jira issue to keep the ticket up to date.',
    input_schema={'type': 'object', 'properties': {'issue_key': {'type': 'string', 'description': 'Jira issue key to comment on (e.g. OPS-123)'}, 'body': {'type': 'string', 'description': 'Comment text with investigation findings'}}, 'required': ['issue_key', 'body']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'email', 'api_token', 'project_key'),
    requires=['base_url', 'email', 'api_token', 'issue_key', 'body'],
    use_cases=['Appending root cause analysis findings to an existing incident ticket', 'Posting investigation status updates on a Jira issue', 'Adding evidence or log excerpts as a comment for the incident responders', 'Documenting resolution steps on the tracking ticket'],
)
def jira_add_comment(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.JiraAddCommentTool',
            attr='jira_add_comment',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"jira_add_comment failed: {exc}"}
