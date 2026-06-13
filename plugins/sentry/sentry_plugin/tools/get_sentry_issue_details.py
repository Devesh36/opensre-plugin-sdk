"""Bridged tool: get_sentry_issue_details (from OpenSRE app.tools.SentryIssueDetailsTool)."""

from __future__ import annotations

from typing import Any

from sentry_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_sentry_issue_details',
    source='sentry',
    description='Fetch full details for a Sentry issue.',
    input_schema={'type': 'object', 'properties': {'issue_id': {'type': 'string'}}, 'required': ['issue_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('organization_slug', 'sentry_token', 'sentry_url', 'project_slug'),
    requires=['organization_slug', 'sentry_token', 'issue_id'],
    use_cases=['Inspecting the main error group linked to an alert', 'Reviewing culprit, level, and regression details', 'Understanding whether an incident matches an existing issue'],
)
def get_sentry_issue_details(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SentryIssueDetailsTool',
            attr='get_sentry_issue_details',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_sentry_issue_details failed: {exc}"}
