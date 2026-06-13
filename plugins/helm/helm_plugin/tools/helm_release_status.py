"""Bridged tool: helm_release_status (from OpenSRE app.tools.HelmTools)."""

from __future__ import annotations

from typing import Any

from helm_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='helm_release_status',
    source='helm',
    description='Fetch Helm release status (resources, hooks metadata, notes) as structured JSON.',
    input_schema={'type': 'object', 'properties': {'release_name': {'type': 'string', 'description': 'Helm release name'}, 'namespace': {'type': 'string', 'default': '', 'description': 'Kubernetes namespace for the release (default if empty)'}, 'default_namespace': {'type': 'string', 'default': '', 'description': 'Fallback ns'}, 'integration_id': {'type': 'string', 'default': ''}}, 'required': ['release_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('helm_path', 'kube_context', 'kubeconfig'),
    requires=['release_name'],
    use_cases=['Checking whether a Helm release is in failed/pending state', 'Reading chart/app version and last deployment metadata for a release'],
)
def helm_release_status(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.HelmTools',
            attr='helm_release_status',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"helm_release_status failed: {exc}"}
