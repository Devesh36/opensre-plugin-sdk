"""Bridged tool: list_eks_namespaces (from OpenSRE app.tools.EKSListNamespacesTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_eks_namespaces',
    source='eks',
    description='List all namespaces in the EKS cluster with their status.',
    input_schema={'type': 'object', 'properties': {'cluster_name': {'type': 'string'}, 'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'credentials': {'type': 'object', 'default': None}}, 'required': ['cluster_name', 'role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name'],
    use_cases=['Discovering what namespaces are present before querying pods/deployments', 'Confirming an alert namespace actually exists in the cluster'],
)
def list_eks_namespaces(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSListNamespacesTool',
            attr='list_eks_namespaces',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_eks_namespaces failed: {exc}"}
