"""Bridged tool: opsgenie_alert_detail (from OpenSRE app.tools.OpsGenieAlertDetailTool)."""

from __future__ import annotations

from typing import Any

from opsgenie_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='opsgenie_alert_detail',
    source='opsgenie',
    description='Fetch the full details, description, responder info, and activity log for a specific OpsGenie alert to understand its lifecycle and current triage state.',
    input_schema={'type': 'object', 'properties': {'alert_id': {'type': 'string', 'description': 'OpsGenie alert ID to fetch details for'}, 'include_activity_log': {'type': 'boolean', 'default': True, 'description': 'Whether to also fetch the alert activity log'}, 'log_limit': {'type': 'integer', 'default': 20, 'description': 'Maximum number of activity log entries to fetch'}}, 'required': ['alert_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'region'),
    requires=['api_key', 'alert_id'],
    use_cases=['Getting the full description and context of an OpsGenie alert', 'Checking who acknowledged or responded to an alert', 'Reviewing the activity timeline for an alert during an incident', 'Reading alert details (custom fields, tags, entity) for RCA context'],
)
def opsgenie_alert_detail(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.OpsGenieAlertDetailTool',
            attr='opsgenie_alert_detail',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"opsgenie_alert_detail failed: {exc}"}
