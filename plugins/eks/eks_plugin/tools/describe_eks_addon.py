"""Bridged tool: describe_eks_addon (from OpenSRE app.tools.EKSDescribeAddonTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='describe_eks_addon',
    source='eks',
    description='Describe an EKS addon — coredns, kube-proxy, vpc-cni, aws-ebs-csi-driver, etc.',
    input_schema={'type': 'object', 'properties': {'cluster_name': {'type': 'string'}, 'addon_name': {'type': 'string', 'default': 'coredns'}, 'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'credentials': {'type': 'object', 'default': None}}, 'required': ['cluster_name', 'role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name'],
    use_cases=['Investigating DNS resolution failures (coredns)', 'Checking networking issues (vpc-cni)', 'Finding storage attachment failures (ebs-csi)'],
)
def describe_eks_addon(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSDescribeAddonTool',
            attr='describe_eks_addon',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"describe_eks_addon failed: {exc}"}
