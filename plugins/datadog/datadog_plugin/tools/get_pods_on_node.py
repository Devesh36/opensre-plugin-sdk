"""Bridged tool: get_pods_on_node (from OpenSRE app.tools.DataDogNodePodsTool)."""

from __future__ import annotations

from typing import Any

from datadog_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_pods_on_node',
    source='datadog',
    description='Resolve a node IP address to all pods running on that node via Datadog.',
    input_schema={'type': 'object', 'properties': {'node_ip': {'type': 'string', 'description': "The IP address of the node (e.g. '10.0.1.42')"}, 'time_range_minutes': {'type': 'integer', 'default': 60}, 'limit': {'type': 'integer', 'default': 200}}, 'required': ['node_ip']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'app_key', 'site'),
    requires=[],
    use_cases=['Mapping a node IP from an infrastructure alert to specific pods', 'Discovering what pods were running on a failed node', 'Feeding pod names into log retrieval tools for further investigation'],
)
def get_pods_on_node(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DataDogNodePodsTool',
            attr='get_pods_on_node',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_pods_on_node failed: {exc}"}
