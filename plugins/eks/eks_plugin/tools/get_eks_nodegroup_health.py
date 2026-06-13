"""Bridged tool: get_eks_nodegroup_health (from OpenSRE app.tools.EKSNodegroupHealthTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_eks_nodegroup_health',
    source='eks',
    description='Get EKS node group health — instance types, scaling config, AMI version, health issues.',
    input_schema={'type': 'object', 'properties': {'cluster_name': {'type': 'string'}, 'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'nodegroup_name': {'type': 'string'}, 'credentials': {'type': 'object', 'default': None}}, 'required': ['cluster_name', 'role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name'],
    use_cases=['Investigating when pods are unschedulable or nodes are NotReady', 'Checking node capacity and scaling configuration', 'Finding AMI version issues in EKS node groups'],
)
def get_eks_nodegroup_health(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSNodegroupHealthTool',
            attr='get_eks_nodegroup_health',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_eks_nodegroup_health failed: {exc}"}
