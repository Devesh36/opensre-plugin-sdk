"""Bridged tool: list_sentry_issue_events (from OpenSRE app.tools.SentryIssueEventsTool)."""

from __future__ import annotations

from typing import Any

from sentry_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_sentry_issue_events',
    source='sentry',
    description='List recent events for a Sentry issue.',
    input_schema={'type': 'object', 'properties': {'issue_id': {'type': 'string'}, 'limit': {'type': 'integer', 'default': 10}}, 'required': ['issue_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('organization_slug', 'sentry_token', 'sentry_url', 'project_slug'),
    requires=['organization_slug', 'sentry_token', 'issue_id'],
    use_cases=['Reviewing the latest stack traces attached to an issue', 'Checking whether new events appeared during an incident window', 'Comparing repeated failures grouped under the same issue'],
)
def list_sentry_issue_events(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SentryIssueEventsTool',
            attr='list_sentry_issue_events',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_sentry_issue_events failed: {exc}"}
