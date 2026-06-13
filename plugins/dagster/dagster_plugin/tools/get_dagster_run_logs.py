"""Bridged tool: get_dagster_run_logs (from OpenSRE app.tools.DagsterRunLogsTool)."""

from __future__ import annotations

from typing import Any

from dagster_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_dagster_run_logs',
    source='dagster',
    description='Fetch event logs and error details for a specific Dagster run. IMPORTANT: a single run may contain MULTIPLE step failures if ops ran in parallel and several failed independently. The response includes a top-level `summary.failures` list that pre-counts and pre-classifies each step failure (step_key, exception_class, cause_message). Always check `summary.failure_count` first; if it is greater than 1, surface ALL failures in your diagnosis as distinct root causes, do not pick only one. The underlying user-code exception lives in `cause_message` (the wrapper is always a generic DagsterExecutionStepExecutionError). If `summary.truncated` is true, the run produced more events than the inspection cap (`summary.events_examined`); treat the failure_count as a LOWER BOUND and hedge your diagnosis. If `summary.fetch_error` is set, a mid-pagination error stopped the fetch early; the failures shown are a partial set.',
    input_schema={'type': 'object', 'properties': {'run_id': {'type': 'string'}}, 'required': ['run_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('endpoint', 'api_token'),
    requires=[],
    use_cases=[],
)
def get_dagster_run_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DagsterRunLogsTool',
            attr='get_dagster_run_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_dagster_run_logs failed: {exc}"}
