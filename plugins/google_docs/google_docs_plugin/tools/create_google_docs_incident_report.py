"""Bridged tool: create_google_docs_incident_report (from OpenSRE app.tools.GoogleDocsCreateReportTool)."""

from __future__ import annotations

from typing import Any

from google_docs_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='create_google_docs_incident_report',
    source='google_docs',
    description='Create a structured incident postmortem report in Google Docs with investigation findings.',
    input_schema={'type': 'object', 'properties': {'summary': {'type': 'string', 'description': 'Executive summary of the incident'}, 'root_cause': {'type': 'string', 'description': 'Root cause analysis'}, 'evidence': {'type': 'array', 'description': 'List of evidence items with title and description', 'items': {'type': 'object', 'properties': {'description': {'type': 'string'}}}}, 'timeline': {'type': 'array', 'description': 'Timeline of incident events', 'items': {'type': 'object', 'properties': {'time': {'type': 'string'}, 'description': {'type': 'string'}}}}, 'severity': {'type': 'string', 'description': 'Incident severity (critical, high, medium, low)', 'enum': ['critical', 'high', 'medium', 'low']}, 'remediation_steps': {'type': 'array', 'description': 'Steps taken to remediate the incident', 'items': {'type': 'string'}}, 'follow_up_actions': {'type': 'array', 'description': 'Follow-up action items', 'items': {'type': 'string'}}, 'share_with': {'type': 'array', 'description': 'List of email addresses to share the document with', 'items': {'type': 'string'}}, 'share_role': {'type': 'string', 'description': 'Permission role for shared users (reader, writer, owner). Default is writer.', 'enum': ['reader', 'writer', 'owner'], 'default': 'writer'}}, 'required': ['title', 'summary', 'root_cause', 'severity']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('credentials_file', 'folder_id'),
    requires=['google_docs'],
    use_cases=['Generate a shareable incident report after investigation completes', 'Create a collaborative postmortem document for team review', 'Document root cause and remediation steps for stakeholders'],
)
def create_google_docs_incident_report(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.GoogleDocsCreateReportTool',
            attr='create_google_docs_incident_report',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"create_google_docs_incident_report failed: {exc}"}
