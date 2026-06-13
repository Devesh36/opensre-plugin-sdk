"""Bridged tool: list_eks_clusters (from OpenSRE app.tools.EKSListClustersTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_eks_clusters',
    source='eks',
    description='List EKS clusters in the AWS account.',
    input_schema={'type': 'object', 'properties': {'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'cluster_names': {'type': 'array', 'items': {'type': 'string'}}, 'credentials': {'type': 'object', 'default': None}}, 'required': ['role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=[],
    use_cases=['Discovering what EKS clusters exist in the account', 'Confirming a cluster name before running other EKS actions'],
)
def list_eks_clusters(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSListClustersTool',
            attr='list_eks_clusters',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_eks_clusters failed: {exc}"}
