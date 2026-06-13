"""Bridged tool: prefect_flow_runs (from OpenSRE app.tools.PrefectFlowRunsTool)."""

from __future__ import annotations

from typing import Any

from prefect_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='prefect_flow_runs',
    source='prefect',
    description='Fetch recent Prefect flow runs filtered by state, and retrieve logs for failed runs to surface orchestration failures and root-cause evidence.',
    input_schema={'type': 'object', 'properties': {'api_url': {'type': 'string', 'description': 'Prefect API base URL. Use https://api.prefect.cloud/api for Prefect Cloud or your self-hosted server URL (e.g. http://localhost:4200/api).'}, 'account_id': {'type': 'string', 'default': '', 'description': 'Prefect Cloud account ID (required for Prefect Cloud).'}, 'workspace_id': {'type': 'string', 'default': '', 'description': 'Prefect Cloud workspace ID (required for Prefect Cloud).'}, 'states': {'type': 'array', 'items': {'type': 'string'}, 'default': ['FAILED', 'CRASHED'], 'description': 'Flow run states to filter on. Defaults to FAILED and CRASHED.'}, 'limit': {'type': 'integer', 'default': 20, 'description': 'Maximum number of flow runs to return.'}, 'fetch_logs_for_run_id': {'type': 'string', 'default': '', 'description': 'Optional flow run ID to fetch detailed logs for. Use after identifying a specific failed run.'}, 'log_limit': {'type': 'integer', 'default': 100, 'description': 'Maximum number of log lines to fetch per flow run.'}}, 'required': ['api_url']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key',),
    requires=['api_url'],
    use_cases=['Investigating why a Prefect flow run failed or crashed', 'Listing all recent FAILED or CRASHED flow runs for triage', 'Fetching logs from a specific failed flow run', 'Correlating Prefect flow failures with infrastructure alerts', 'Identifying recurring flow failures across deployments'],
)
def prefect_flow_runs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.PrefectFlowRunsTool',
            attr='prefect_flow_runs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"prefect_flow_runs failed: {exc}"}
