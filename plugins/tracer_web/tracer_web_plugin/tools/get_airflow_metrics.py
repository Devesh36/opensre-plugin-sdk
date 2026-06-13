"""Bridged tool: get_airflow_metrics (from OpenSRE app.tools.TracerAirflowMetricsTool)."""

from __future__ import annotations

from typing import Any

from tracer_web_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_airflow_metrics',
    source='tracer_web',
    description='Get Airflow orchestration metrics for the run.',
    input_schema={'type': 'object', 'properties': {'trace_id': {'type': 'string'}}, 'required': ['trace_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('jwt_token', 'api_url'),
    requires=['trace_id'],
    use_cases=['Understanding orchestration issues', 'Identifying workflow problems', 'Proving scheduling hypothesis'],
)
def get_airflow_metrics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerAirflowMetricsTool',
            attr='get_airflow_metrics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_airflow_metrics failed: {exc}"}
