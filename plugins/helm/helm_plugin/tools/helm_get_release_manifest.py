"""Bridged tool: helm_get_release_manifest (from OpenSRE app.tools.HelmTools)."""

from __future__ import annotations

from typing import Any

from helm_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='helm_get_release_manifest',
    source='helm',
    description='Fetch the rendered Kubernetes manifest YAML for a Helm release (truncated if huge).',
    input_schema={'type': 'object', 'properties': {'release_name': {'type': 'string'}, 'namespace': {'type': 'string', 'default': ''}, 'default_namespace': {'type': 'string', 'default': ''}, 'integration_id': {'type': 'string', 'default': ''}}, 'required': ['release_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('helm_path', 'kube_context', 'kubeconfig'),
    requires=['release_name'],
    use_cases=['Inspecting live rendered resources for a chart after an upgrade incident', 'Finding unexpected resources created by a Helm release'],
)
def helm_get_release_manifest(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.HelmTools',
            attr='helm_get_release_manifest',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"helm_get_release_manifest failed: {exc}"}
