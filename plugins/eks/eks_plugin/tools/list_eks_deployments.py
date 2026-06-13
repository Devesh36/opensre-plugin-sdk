"""Bridged tool: list_eks_deployments (from OpenSRE app.tools.EKSListDeploymentsTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_eks_deployments',
    source='eks',
    description='List all deployments in a namespace with replica counts and availability status.',
    input_schema={'type': 'object', 'properties': {'cluster_name': {'type': 'string'}, 'namespace': {'type': 'string', 'description': "Use 'all' for all namespaces"}, 'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'credentials': {'type': 'object', 'default': None}}, 'required': ['cluster_name', 'namespace', 'role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name'],
    use_cases=['Discovering what deployments exist and which are degraded/unavailable', 'Scanning all namespaces for degraded deployments'],
)
def list_eks_deployments(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSListDeploymentsTool',
            attr='list_eks_deployments',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_eks_deployments failed: {exc}"}
