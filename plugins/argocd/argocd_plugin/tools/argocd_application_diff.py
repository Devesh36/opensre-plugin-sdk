"""Bridged tool: argocd_application_diff (from OpenSRE app.tools.ArgoCDApplicationDiffTool)."""

from __future__ import annotations

from typing import Any

from argocd_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='argocd_application_diff',
    source='argocd',
    description='Fetch Argo CD server-side diff output and report whether live cluster state has drifted from the desired GitOps state.',
    input_schema={'type': 'object', 'properties': {'application_name': {'type': 'string', 'description': 'Application name'}, 'project': {'type': 'string', 'default': '', 'description': 'Optional Argo CD project'}, 'app_namespace': {'type': 'string', 'default': '', 'description': 'Optional app namespace'}, 'verify_ssl': {'type': 'boolean', 'default': True, 'description': 'Verify TLS certificates'}}, 'required': ['application_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('base_url', 'bearer_token', 'username', 'password', 'auth_token'),
    requires=['base_url', 'application_name'],
    use_cases=['Detecting GitOps drift during an incident', 'Checking whether an OutOfSync application has Kubernetes object diffs', 'Correlating deployment drift with application health degradation'],
)
def argocd_application_diff(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.ArgoCDApplicationDiffTool',
            attr='argocd_application_diff',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"argocd_application_diff failed: {exc}"}
