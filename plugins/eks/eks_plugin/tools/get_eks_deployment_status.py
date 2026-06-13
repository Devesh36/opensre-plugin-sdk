"""Bridged tool: get_eks_deployment_status (from OpenSRE app.tools.EKSDeploymentStatusTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_eks_deployment_status',
    source='eks',
    description='Get EKS deployment rollout status — desired vs ready vs unavailable replicas.',
    input_schema={'type': 'object', 'properties': {'cluster_name': {'type': 'string'}, 'namespace': {'type': 'string'}, 'deployment_name': {'type': 'string'}, 'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'credentials': {'type': 'object', 'default': None}}, 'required': ['cluster_name', 'namespace', 'deployment_name', 'role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name', 'deployment_name'],
    use_cases=['Checking if a deployment has unavailable replicas', 'Verifying rollout status after a deployment change'],
)
def get_eks_deployment_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSDeploymentStatusTool',
            attr='get_eks_deployment_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_eks_deployment_status failed: {exc}"}
