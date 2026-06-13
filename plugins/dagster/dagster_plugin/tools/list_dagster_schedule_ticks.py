"""Bridged tool: list_dagster_schedule_ticks (from OpenSRE app.tools.DagsterSchedulesTool)."""

from __future__ import annotations

from typing import Any

from dagster_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_dagster_schedule_ticks',
    source='dagster',
    description='Fetch recent tick history for a Dagster schedule. The schedule is identified by all three ScheduleSelector coordinates: repository location name, repository name, and schedule name.',
    input_schema={'type': 'object', 'properties': {'repository_name': {'type': 'string'}, 'repository_location_name': {'type': 'string'}, 'schedule_name': {'type': 'string'}, 'limit': {'type': 'integer'}}, 'required': ['repository_name', 'repository_location_name', 'schedule_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('endpoint', 'api_token'),
    requires=[],
    use_cases=[],
)
def list_dagster_schedule_ticks(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DagsterSchedulesTool',
            attr='list_dagster_schedule_ticks',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_dagster_schedule_ticks failed: {exc}"}
