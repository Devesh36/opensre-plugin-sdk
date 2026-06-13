"""Bridged tool: helm_get_release_values (from OpenSRE app.tools.HelmTools)."""

from __future__ import annotations

from typing import Any

from helm_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='helm_get_release_values',
    source='helm',
    description='Fetch Helm values for a release as JSON. May include secrets — handle carefully.',
    input_schema={'type': 'object', 'properties': {'release_name': {'type': 'string'}, 'namespace': {'type': 'string', 'default': ''}, 'default_namespace': {'type': 'string', 'default': ''}, 'all_values': {'type': 'boolean', 'default': False, 'description': 'When true, pass --all to include computed defaults'}, 'integration_id': {'type': 'string', 'default': ''}}, 'required': ['release_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('helm_path', 'kube_context', 'kubeconfig'),
    requires=['release_name'],
    use_cases=['Confirming image tags, replica counts, or feature flags shipped with a chart revision', 'Comparing effective values against manifest during a misconfiguration investigation'],
)
def helm_get_release_values(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.HelmTools',
            attr='helm_get_release_values',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"helm_get_release_values failed: {exc}"}
