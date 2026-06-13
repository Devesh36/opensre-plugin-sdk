"""Bridged tool: get_cloudwatch_batch_metrics (from OpenSRE app.tools.CloudWatchBatchMetricsTool)."""

from __future__ import annotations

from typing import Any

from cloudwatch_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_cloudwatch_batch_metrics',
    source='cloudwatch',
    description='Get CloudWatch metrics for AWS Batch jobs.',
    input_schema={'type': 'object', 'properties': {'job_queue': {'type': 'string', 'description': 'The AWS Batch job queue name'}, 'metric_type': {'type': 'string', 'enum': ['cpu', 'memory'], 'default': 'cpu'}, 'limit': {'type': 'integer', 'default': 50, 'description': 'Maximum number of metric data points to return'}}, 'required': ['job_queue']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['job_queue'],
    use_cases=['Proving resource constraint hypothesis', 'Understanding batch job performance', 'Identifying AWS infrastructure issues'],
)
def get_cloudwatch_batch_metrics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.CloudWatchBatchMetricsTool',
            attr='get_cloudwatch_batch_metrics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_cloudwatch_batch_metrics failed: {exc}"}
