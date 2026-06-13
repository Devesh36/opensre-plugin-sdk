"""Bridged tool: search_sentry_issues (from OpenSRE app.tools.SentrySearchIssuesTool)."""

from __future__ import annotations

from typing import Any

from sentry_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='search_sentry_issues',
    source='sentry',
    description='Search Sentry issues related to an incident or failure signature.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string', 'default': ''}, 'limit': {'type': 'integer', 'default': 10}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('organization_slug', 'sentry_token', 'sentry_url', 'project_slug'),
    requires=['organization_slug', 'sentry_token'],
    use_cases=['Checking whether an alert maps to a known Sentry issue', 'Finding unresolved error groups for a service or environment', 'Looking up recent crash reports that match an incident symptom'],
)
def search_sentry_issues(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SentrySearchIssuesTool',
            attr='search_sentry_issues',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"search_sentry_issues failed: {exc}"}
