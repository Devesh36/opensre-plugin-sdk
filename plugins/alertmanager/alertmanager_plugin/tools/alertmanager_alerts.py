"""Bridged tool: alertmanager_alerts (from OpenSRE app.tools.AlertmanagerAlertsTool)."""

from __future__ import annotations

from typing import Any

from alertmanager_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='alertmanager_alerts',
    source='alertmanager',
    description='Query Alertmanager to list firing, silenced, and inhibited alerts. Use this to discover concurrent alerts that may share a root cause, check whether a known alert is already silenced, or understand the full alert landscape during an incident.',
    input_schema={'type': 'object', 'properties': {'active': {'type': 'boolean', 'default': True, 'description': 'Include active (firing) alerts'}, 'silenced': {'type': 'boolean', 'default': False, 'description': 'Include silenced alerts'}, 'inhibited': {'type': 'boolean', 'default': False, 'description': 'Include inhibited alerts'}, 'filter_labels': {'type': 'array', 'items': {'type': 'string'}, 'default': [], 'description': 'Label matchers to filter alerts (e.g. ["alertname=\\"HighErrorRate\\""])'}, 'limit': {'type': 'integer', 'default': 50, 'description': 'Maximum number of alerts to return'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'bearer_token', 'username', 'password'),
    requires=['base_url'],
    use_cases=['Listing all currently firing alerts to identify correlated incidents', 'Checking whether alerts matching specific labels are active or silenced', 'Correlating a Prometheus alert with other concurrent signals (OOM, latency, errors)', 'Determining the blast radius of an infrastructure change via active alert labels'],
)
def alertmanager_alerts(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AlertmanagerAlertsTool',
            attr='alertmanager_alerts',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"alertmanager_alerts failed: {exc}"}
