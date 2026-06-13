"""Bridged tool: argocd_application_status (from OpenSRE app.tools.ArgoCDApplicationStatusTool)."""

from __future__ import annotations

from typing import Any

from argocd_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='argocd_application_status',
    source='argocd',
    description='Fetch Argo CD application sync status, health status, current revision, and recent deployment history.',
    input_schema={'type': 'object', 'properties': {'application_name': {'type': 'string', 'default': '', 'description': 'Application name'}, 'project': {'type': 'string', 'default': '', 'description': 'Optional Argo CD project'}, 'app_namespace': {'type': 'string', 'default': '', 'description': 'Optional app namespace'}, 'verify_ssl': {'type': 'boolean', 'default': True, 'description': 'Verify TLS certificates'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'bearer_token', 'username', 'password', 'auth_token'),
    requires=['base_url'],
    use_cases=['Checking whether a GitOps application is OutOfSync or Degraded', 'Correlating an incident with a recent Argo CD deployment revision', 'Listing visible Argo CD applications when an alert omits the application name'],
)
def argocd_application_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.ArgoCDApplicationStatusTool',
            attr='argocd_application_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"argocd_application_status failed: {exc}"}
