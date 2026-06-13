"""Bridged tool: get_eks_pod_logs (from OpenSRE app.tools.EKSPodLogsTool)."""

from __future__ import annotations

from typing import Any

from eks_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_eks_pod_logs',
    source='eks',
    description='Fetch logs from a specific EKS pod.',
    input_schema={'type': 'object', 'properties': {'cluster_name': {'type': 'string'}, 'namespace': {'type': 'string'}, 'pod_name': {'type': 'string'}, 'role_arn': {'type': 'string'}, 'external_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'credentials': {'type': 'object', 'default': None}, 'tail_lines': {'type': 'integer', 'default': 100}}, 'required': ['cluster_name', 'namespace', 'pod_name', 'role_arn']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['cluster_name', 'pod_name'],
    use_cases=['Fetching crash logs from a specific pod', 'Reviewing application output for a known failing pod'],
)
def get_eks_pod_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EKSPodLogsTool',
            attr='get_eks_pod_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_eks_pod_logs failed: {exc}"}
