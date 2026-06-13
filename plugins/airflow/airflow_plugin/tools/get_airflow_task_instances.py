"""Bridged tool: get_airflow_task_instances (from OpenSRE app.tools.TracerAirflowDAGTool)."""

from __future__ import annotations

from typing import Any

from airflow_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_airflow_task_instances',
    source='airflow',
    description='Fetch Airflow task instances for a specific DAG run.',
    input_schema={'type': 'object', 'properties': {'dag_id': {'type': 'string'}, 'dag_run_id': {'type': 'string'}}, 'required': ['dag_id', 'dag_run_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'username', 'password', 'auth_token'),
    requires=['dag_id', 'dag_run_id'],
    use_cases=['Inspecting failed Airflow task instances', 'Finding task-level failure evidence', 'Grounding RCA in Airflow task state'],
)
def get_airflow_task_instances(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerAirflowDAGTool',
            attr='get_airflow_task_instances',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_airflow_task_instances failed: {exc}"}
