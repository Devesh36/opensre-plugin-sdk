"""Bridged tool: describe_rds_instance (from OpenSRE app.tools.RDSDescribeInstanceTool)."""

from __future__ import annotations

from typing import Any

from rds_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='describe_rds_instance',
    source='rds',
    description='Describe an AWS RDS database instance — engine, version, status, storage, Multi-AZ, endpoint, and parameter groups.',
    input_schema={'properties': {'db_instance_identifier': {'description': 'RDS DB instance identifier, for example `prod-orders-db`.', 'type': 'string'}, 'region': {'default': 'us-east-1', 'description': 'AWS region where the RDS instance is deployed.', 'type': 'string'}}, 'required': ['db_instance_identifier'], 'type': 'object', 'additionalProperties': False},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['db_instance_identifier'],
    use_cases=['Investigating instance-level issues: status, availability, engine version', 'Checking if Multi-AZ is enabled or storage is misconfigured', 'Verifying RDS instance status (available, modifying, failed)'],
)
def describe_rds_instance(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.RDSDescribeInstanceTool',
            attr='describe_rds_instance',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"describe_rds_instance failed: {exc}"}
