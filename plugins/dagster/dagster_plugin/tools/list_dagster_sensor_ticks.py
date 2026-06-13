"""Bridged tool: list_dagster_sensor_ticks (from OpenSRE app.tools.DagsterSensorsTool)."""

from __future__ import annotations

from typing import Any

from dagster_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_dagster_sensor_ticks',
    source='dagster',
    description='Fetch recent tick history for a Dagster sensor. The sensor is identified by all three SensorSelector coordinates: repository location name, repository name, and sensor name.',
    input_schema={'type': 'object', 'properties': {'repository_name': {'type': 'string'}, 'repository_location_name': {'type': 'string'}, 'sensor_name': {'type': 'string'}, 'limit': {'type': 'integer'}}, 'required': ['repository_name', 'repository_location_name', 'sensor_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('endpoint', 'api_token'),
    requires=[],
    use_cases=[],
)
def list_dagster_sensor_ticks(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DagsterSensorsTool',
            attr='list_dagster_sensor_ticks',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_dagster_sensor_ticks failed: {exc}"}
