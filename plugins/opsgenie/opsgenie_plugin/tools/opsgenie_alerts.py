"""Bridged tool: opsgenie_alerts (from OpenSRE app.tools.OpsGenieAlertsTool)."""

from __future__ import annotations

from typing import Any

from opsgenie_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='opsgenie_alerts',
    source='opsgenie',
    description='Search OpsGenie alerts to find active incidents, identify unacknowledged P1/P2 alerts, and correlate alert context with errors from Datadog, Sentry, or other sources.',
    input_schema={'type': 'object', 'properties': {'query': {'type': 'string', 'default': '', 'description': 'OpsGenie alert search query (e.g. status=open, tag=env:prod)'}, 'limit': {'type': 'integer', 'default': 20, 'description': 'Maximum number of alerts to return'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'region'),
    requires=['api_key'],
    use_cases=['Listing open OpsGenie alerts for an ongoing incident', 'Finding unacknowledged high-priority alerts', 'Correlating an OpsGenie alert with errors in Datadog or Sentry', 'Checking recent alert history for a service or tag'],
)
def opsgenie_alerts(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpsGenieAlertsTool',
            attr='opsgenie_alerts',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"opsgenie_alerts failed: {exc}"}
