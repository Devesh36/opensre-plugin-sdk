"""Bridged tool: list_eks_pods (from OpenSRE app.tools.EKSListPodsTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_eks_pods',
    source='eks',
    description='List all pods in a namespace with their status, phase, restart counts, and conditions.',
    input_schema={'properties': {'cluster_name': {'description': 'EKS cluster name.', 'type': 'string'}, 'namespace': {'description': 'Kubernetes namespace to inspect, or `all` for every namespace.', 'type': 'string'}, 'region': {'default': 'us-east-1', 'description': 'AWS region of the EKS cluster.', 'type': 'string'}}, 'required': ['cluster_name', 'namespace'], 'type': 'object', 'additionalProperties': False},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name'],
    use_cases=['Discovering what pods exist before fetching logs', 'Finding which pods are crashing, pending, or failed', 'Checking restart counts for crash-looping containers'],
)
def list_eks_pods(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSListPodsTool',
            attr='list_eks_pods',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_eks_pods failed: {exc}"}
