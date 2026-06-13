"""Bridged tool: execute_aws_operation (from OpenSRE app.tools.AWSOperationTool)."""

from __future__ import annotations

from typing import Any

from aws_sdk_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='execute_aws_operation',
    source='aws_sdk',
    description='Execute any read-only AWS SDK operation for investigation.',
    input_schema={'type': 'object', 'properties': {'service': {'type': 'string', 'description': "AWS service name (e.g., 'ecs', 'rds', 'ec2', 'lambda')"}, 'operation': {'type': 'string', 'description': "Operation name (e.g., 'describe_tasks', 'get_role')"}, 'parameters': {'type': 'object', 'description': 'Operation parameters as dict'}}, 'required': ['service', 'operation']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['service', 'operation'],
    use_cases=['Checking ECS task status and health (ecs.describe_tasks)', 'Inspecting RDS database configuration (rds.describe_db_instances)', 'Reviewing VPC networking setup (ec2.describe_vpcs)', 'Examining IAM role permissions (iam.get_role)', 'Investigating EC2 instance state (ec2.describe_instances)', 'Querying CloudFormation stack details (cloudformation.describe_stacks)', 'Checking EFS mount targets (efs.describe_mount_targets)', 'Reviewing Systems Manager parameters (ssm.get_parameter)', 'Inspecting Step Functions executions (stepfunctions.describe_execution)', 'Checking Secrets Manager secrets metadata (secretsmanager.describe_secret)'],
)
def execute_aws_operation(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.AWSOperationTool',
            attr='execute_aws_operation',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"execute_aws_operation failed: {exc}"}
