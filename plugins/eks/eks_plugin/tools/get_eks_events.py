"""Bridged tool: get_eks_events (from OpenSRE app.tools.EKSEventsTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_eks_events',
    source='eks',
    description='Get Kubernetes Warning events in a namespace.',
    input_schema={'type': 'object', 'properties': {'cluster_name': {'type': 'string'}, 'namespace': {'type': 'string', 'description': "Use 'all' for all namespaces"}, 'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'credentials': {'type': 'object', 'default': None}}, 'required': ['cluster_name', 'namespace', 'role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name'],
    use_cases=['Finding OOMKilled, FailedScheduling, BackOff, Unhealthy, FailedMount events', 'Understanding what Kubernetes reported during an incident'],
)
def get_eks_events(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSEventsTool',
            attr='get_eks_events',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_eks_events failed: {exc}"}
