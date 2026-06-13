"""Bridged tool: get_sre_guidance (from OpenSRE app.tools.SREGuidanceTool)."""

from __future__ import annotations

from typing import Any

from knowledge_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_sre_guidance',
    source='knowledge',
    description='Retrieve SRE best practices for data pipeline incidents.',
    input_schema={'type': 'object', 'properties': {'topic': {'type': 'string', 'description': 'Specific topic: pipeline_types, slo_freshness, slo_correctness, failure_delayed_data, failure_corrupt_data, hotspotting, thundering_herd, monitoring_pipelines, dependency_failure, recovery_remediation, resource_planning, pipeline_documentation, playbooks_overview, workflow_patterns'}, 'keywords': {'type': 'array', 'items': {'type': 'string'}, 'description': "Keywords to match against SRE content (e.g., ['timeout', 'delay'])"}, 'max_topics': {'type': 'integer', 'default': 3}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=[],
    use_cases=['Understanding pipeline failure patterns (delayed data, corrupt data)', 'Applying SLO concepts to data freshness and correctness issues', 'Identifying hotspotting and resource contention patterns', 'Getting remediation guidance for common pipeline failures', 'Structuring postmortem findings and recommendations'],
)
def get_sre_guidance(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SREGuidanceTool',
            attr='get_sre_guidance',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_sre_guidance failed: {exc}"}
