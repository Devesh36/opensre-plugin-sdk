"""Bridged tool: prefect_worker_health (from OpenSRE app.tools.PrefectWorkerHealthTool)."""

from __future__ import annotations

from typing import Any

from prefect_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='prefect_worker_health',
    source='prefect',
    description='Inspect Prefect work pools and their registered workers to identify offline, unhealthy, or paused workers that may be blocking flow run execution.',
    input_schema={'type': 'object', 'properties': {'api_url': {'type': 'string', 'description': 'Prefect API base URL. Use https://api.prefect.cloud/api for Prefect Cloud or your self-hosted server URL (e.g. http://localhost:4200/api).'}, 'account_id': {'type': 'string', 'default': '', 'description': 'Prefect Cloud account ID (required for Prefect Cloud).'}, 'workspace_id': {'type': 'string', 'default': '', 'description': 'Prefect Cloud workspace ID (required for Prefect Cloud).'}, 'work_pool_name': {'type': 'string', 'default': '', 'description': 'Name of a specific work pool to inspect workers for. If omitted, lists all work pools without drilling into workers.'}, 'pool_limit': {'type': 'integer', 'default': 20, 'description': 'Maximum number of work pools to list.'}, 'worker_limit': {'type': 'integer', 'default': 20, 'description': 'Maximum number of workers to list per work pool.'}}, 'required': ['api_url']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('api_key',),
    requires=['api_url'],
    use_cases=['Diagnosing why Prefect flows are stuck in PENDING state', 'Identifying offline or unresponsive Prefect workers', 'Checking which work pools are paused or have no active workers', 'Investigating worker heartbeat failures', 'Auditing work pool concurrency limits during incident investigation'],
)
def prefect_worker_health(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.PrefectWorkerHealthTool',
            attr='prefect_worker_health',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"prefect_worker_health failed: {exc}"}
