"""Bridged tool: describe_rds_events (from OpenSRE app.tools.RDSEventsTool)."""

from __future__ import annotations

from typing import Any

from rds_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='describe_rds_events',
    source='rds',
    description='Describe recent AWS RDS events for a DB instance — failovers, maintenance windows, parameter changes, and backup events.',
    input_schema={'type': 'object', 'properties': {'db_instance_identifier': {'type': 'string'}, 'region': {'type': 'string', 'default': 'us-east-1'}, 'duration_minutes': {'type': 'integer', 'default': 60, 'minimum': 1, 'maximum': 20160}}, 'required': ['db_instance_identifier']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=['db_instance_identifier'],
    use_cases=['Investigating Multi-AZ failover events', 'Checking recent maintenance or parameter group changes', 'Tracing backup or recovery events around an incident'],
)
def describe_rds_events(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.RDSEventsTool',
            attr='describe_rds_events',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"describe_rds_events failed: {exc}"}
