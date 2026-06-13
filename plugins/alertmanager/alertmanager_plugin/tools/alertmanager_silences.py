"""Bridged tool: alertmanager_silences (from OpenSRE app.tools.AlertmanagerSilencesTool)."""

from __future__ import annotations

from typing import Any

from alertmanager_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='alertmanager_silences',
    source='alertmanager',
    description='Query Alertmanager silences to see which alerts are currently suppressed and why. Helps distinguish planned maintenance windows from unexpected alert suppression.',
    input_schema={'type': 'object', 'properties': {'limit': {'type': 'integer', 'default': 50, 'description': 'Maximum number of silences to return'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'bearer_token', 'username', 'password'),
    requires=['base_url'],
    use_cases=['Checking whether a firing alert has been silenced (planned maintenance vs real incident)', 'Listing active silences to understand current operational state', 'Determining if an alert is suppressed by an ongoing maintenance window'],
)
def alertmanager_silences(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AlertmanagerSilencesTool',
            attr='alertmanager_silences',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"alertmanager_silences failed: {exc}"}
