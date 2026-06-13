"""Bridged tool: vercel_deployment_logs (from OpenSRE app.tools.VercelLogsTool)."""

from __future__ import annotations

from typing import Any

from vercel_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='vercel_deployment_logs',
    source='vercel',
    description='Fetch build events and serverless function runtime logs for a specific Vercel deployment, useful for diagnosing build failures and runtime errors.',
    input_schema={'type': 'object', 'properties': {'project_id': {'type': 'string', 'default': '', 'description': 'Vercel project ID (scopes runtime logs to the project API)'}, 'deployment_id': {'type': 'string', 'description': 'Vercel deployment ID (uid) to fetch logs for'}, 'include_runtime_logs': {'type': 'boolean', 'default': True, 'description': 'Whether to also fetch serverless function runtime logs'}, 'limit': {'type': 'integer', 'default': 100, 'description': 'Maximum number of log entries to fetch per source'}}, 'required': ['deployment_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_token', 'team_id'),
    requires=['api_token', 'deployment_id'],
    use_cases=['Diagnosing why a Vercel build failed', 'Fetching serverless function stdout/stderr for a deployment', 'Correlating Vercel runtime errors with alerts from Datadog or Sentry', 'Inspecting build output for dependency or compilation errors'],
)
def vercel_deployment_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.VercelLogsTool',
            attr='vercel_deployment_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"vercel_deployment_logs failed: {exc}"}
