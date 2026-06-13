"""Bridged tool: list_dagster_runs (from OpenSRE app.tools.DagsterRunsTool)."""

from __future__ import annotations

from typing import Any

from dagster_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_dagster_runs',
    source='dagster',
    description='List recent Dagster pipeline/job runs with status and duration. When the alert specifies a pipeline name (commonly in its `pipeline`, `alert_name`, or `details.pipeline` field), ALWAYS pass that as `job_name` to scope results. Dagster instances run many pipelines and without the filter you get an interleaved mix from every pipeline that contaminates your evidence. Do not call this tool multiple times trying different filters; set `job_name` once and pair it with `status="FAILURE"` for incident investigations.',
    input_schema={'type': 'object', 'properties': {'limit': {'type': 'integer'}, 'status': {'type': 'string'}, 'job_name': {'type': 'string'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('endpoint', 'api_token'),
    requires=[],
    use_cases=[],
)
def list_dagster_runs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DagsterRunsTool',
            attr='list_dagster_runs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_dagster_runs failed: {exc}"}
