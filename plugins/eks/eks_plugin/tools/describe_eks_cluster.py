"""Bridged tool: describe_eks_cluster (from OpenSRE app.tools.EKSDescribeClusterTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='describe_eks_cluster',
    source='eks',
    description='Describe an EKS cluster — health, version, status, endpoint, logging config.',
    input_schema={'type': 'object', 'properties': {'cluster_name': {'type': 'string'}, 'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'credentials': {'type': 'object', 'default': None}}, 'required': ['cluster_name', 'role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name'],
    use_cases=['Investigating cluster-level issues: version mismatches, endpoint problems', 'Checking if control plane logging is disabled', 'Verifying cluster status (ACTIVE, DEGRADED, FAILED)'],
)
def describe_eks_cluster(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSDescribeClusterTool',
            attr='describe_eks_cluster',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"describe_eks_cluster failed: {exc}"}
