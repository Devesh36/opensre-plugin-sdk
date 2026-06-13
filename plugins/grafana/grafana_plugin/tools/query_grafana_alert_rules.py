"""Bridged tool: query_grafana_alert_rules (from OpenSRE app.tools.GrafanaAlertRulesTool)."""

from __future__ import annotations

from typing import Any

from grafana_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='query_grafana_alert_rules',
    source='grafana',
    description='Query Grafana alert rules to understand what is being monitored.',
    input_schema={'type': 'object', 'properties': {'folder': {'type': 'string'}, 'grafana_endpoint': {'type': 'string'}, 'grafana_api_key': {'type': 'string'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'api_key'),
    requires=[],
    use_cases=['Investigating DatasourceNoData alerts to find the exact PromQL/LogQL query', 'Understanding monitoring configuration and thresholds', 'Auditing which alerts are active for a pipeline'],
)
def query_grafana_alert_rules(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GrafanaAlertRulesTool',
            attr='query_grafana_alert_rules',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"query_grafana_alert_rules failed: {exc}"}
