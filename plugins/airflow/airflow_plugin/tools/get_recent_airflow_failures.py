"""Bridged tool: get_recent_airflow_failures (from OpenSRE app.tools.TracerAirflowDAGTool)."""

from __future__ import annotations

from typing import Any

from airflow_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_recent_airflow_failures',
    source='airflow',
    description='Fetch recent failed or retrying Airflow task evidence for a DAG.',
    input_schema={'type': 'object', 'properties': {'dag_id': {'type': 'string'}, 'limit': {'type': 'integer', 'default': 5}}, 'required': ['dag_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'username', 'password', 'auth_token'),
    requires=['dag_id'],
    use_cases=['Investigating Airflow DAG failures', 'Finding failed or retrying task instances', 'Grounding RCA in Airflow DAG/task evidence'],
)
def get_recent_airflow_failures(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TracerAirflowDAGTool',
            attr='get_recent_airflow_failures',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_recent_airflow_failures failed: {exc}"}
