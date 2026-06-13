"""Bridged tool: get_airflow_dag_runs (from OpenSRE app.tools.TracerAirflowDAGTool)."""

from __future__ import annotations

from typing import Any

from airflow_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_airflow_dag_runs',
    source='airflow',
    description='Fetch recent Airflow DAG runs for a DAG.',
    input_schema={'type': 'object', 'properties': {'dag_id': {'type': 'string'}, 'limit': {'type': 'integer', 'default': 10}, 'state': {'type': 'string'}}, 'required': ['dag_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'username', 'password', 'auth_token'),
    requires=['dag_id'],
    use_cases=['Checking recent Airflow DAG run state', 'Finding failed DAG runs', 'Validating Airflow orchestration state'],
)
def get_airflow_dag_runs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerAirflowDAGTool',
            attr='get_airflow_dag_runs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_airflow_dag_runs failed: {exc}"}
