"""Bridged tool: ec2_instances_by_tag (from OpenSRE app.tools.EC2InstancesByTagTool)."""

from __future__ import annotations

from typing import Any

from ec2_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='ec2_instances_by_tag',
    source='ec2',
    description='List EC2 instances filtered by ``tier`` tag, instance IDs, or VPC. Use to enumerate the application tier(s) behind a load balancer or plausibly driving load on a downstream RDS. Returns a per-tier grouping so correlation with CloudWatch CPU is straightforward.',
    input_schema={'type': 'object', 'properties': {'tier': {'type': 'string', 'description': "tag value for the 'tier' tag"}, 'instance_ids': {'type': 'array', 'items': {'type': 'string'}, 'default': []}, 'vpc_id': {'type': 'string', 'default': ''}, 'region': {'type': 'string', 'default': 'us-east-1'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['region'],
    use_cases=['Discovering EC2 application tiers when investigating a non-K8s alert', 'Mapping a tier name (web/worker/etc.) to its instance IDs', "Bridging EC2 → RDS when answering 'which tier drives DB load'"],
)
def ec2_instances_by_tag(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.EC2InstancesByTagTool',
            attr='ec2_instances_by_tag',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"ec2_instances_by_tag failed: {exc}"}
