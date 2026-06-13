"""Bridged tool: get_elb_target_health (from OpenSRE app.tools.ELBTargetHealthTool)."""

from __future__ import annotations

from typing import Any

from ec2_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_elb_target_health',
    source='ec2',
    description='Describe ELB v2 target groups and the health of their registered targets. Use to map a load balancer or target group to the EC2 instance IDs serving traffic and to identify unhealthy/draining targets.',
    input_schema={'type': 'object', 'properties': {'target_group_arns': {'type': 'array', 'items': {'type': 'string'}, 'default': [], 'description': 'List of target group ARNs (multi-TG ALBs are common).'}, 'target_group_arn': {'type': 'string', 'description': 'Convenience alias for a single target group ARN.'}, 'load_balancer_arn': {'type': 'string'}, 'region': {'type': 'string', 'default': 'us-east-1'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['region'],
    use_cases=['Mapping a target group ARN to the EC2 instances behind it', 'Identifying unhealthy or draining targets correlated with a request-path alert', 'Bridging DNS → LB → EC2 when investigating a non-K8s topology'],
)
def get_elb_target_health(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.ELBTargetHealthTool',
            attr='get_elb_target_health',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_elb_target_health failed: {exc}"}
