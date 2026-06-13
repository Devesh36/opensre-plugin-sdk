"""Bridged tool: incident_io_incidents (from OpenSRE app.tools.IncidentIoIncidentsTool)."""

from __future__ import annotations

from typing import Any

from incident_io_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='incident_io_incidents',
    source='incident_io',
    description='Read incident.io incidents, incident metadata, and incident updates for RCA context. Can append OpenSRE findings to the incident summary through the supported edit endpoint.',
    input_schema={'type': 'object', 'properties': {'action': {'type': 'string', 'enum': ['list', 'get', 'updates', 'context', 'append_summary'], 'default': 'context', 'description': 'Action to perform.'}, 'status_category': {'type': 'string', 'default': 'live', 'description': 'Incident status category for list, e.g. live, triage, learning, or empty for all.'}, 'page_size': {'type': 'integer', 'default': 20, 'description': 'Maximum incidents or updates to return.'}, 'after': {'type': 'string', 'description': 'Pagination cursor from incident.io.'}, 'incident_id': {'type': 'string', 'description': 'incident.io incident ID for get, updates, context, or append_summary.'}, 'body': {'type': 'string', 'description': 'Detailed RCA findings or next steps for append_summary.'}, 'notify_incident_channel': {'type': 'boolean', 'default': False, 'description': 'Whether incident.io should notify the incident channel on summary update.'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key', 'base_url'),
    requires=['api_key'],
    use_cases=['Listing live incident.io incidents related to the current alert', 'Reading incident metadata, custom fields, roles, timestamps, and updates', 'Using incident updates as timeline/status context during RCA', 'Appending investigation findings to the incident summary when explicitly requested'],
)
def incident_io_incidents(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.IncidentIoIncidentsTool',
            attr='incident_io_incidents',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"incident_io_incidents failed: {exc}"}
