"""Bridged tool: vercel_deployment_status (from OpenSRE app.tools.VercelDeploymentStatusTool)."""

from __future__ import annotations

from typing import Any

from vercel_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='vercel_deployment_status',
    source='vercel',
    description='Fetch recent Vercel deployments for a project and surface failed ones with error details, git commit info, and timestamps.',
    input_schema={'type': 'object', 'properties': {'project_id': {'type': 'string', 'default': '', 'description': 'Vercel project ID to scope the query'}, 'limit': {'type': 'integer', 'default': 10, 'description': 'Maximum number of deployments to fetch'}, 'state': {'type': 'string', 'default': '', 'description': 'Filter by state: READY, ERROR, BUILDING, or CANCELED'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_token', 'team_id'),
    requires=['api_token'],
    use_cases=['Checking whether a recent Vercel deployment succeeded or failed', 'Correlating a deployment failure with downstream errors in Datadog or Sentry', 'Identifying which git commit triggered a broken deployment', 'Listing recent deployment history for a Vercel project'],
)
def vercel_deployment_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.VercelDeploymentStatusTool',
            attr='vercel_deployment_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"vercel_deployment_status failed: {exc}"}
