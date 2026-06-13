"""Bridged tool: helm_list_releases (from OpenSRE app.tools.HelmTools)."""

from __future__ import annotations

from typing import Any

from helm_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='helm_list_releases',
    source='helm',
    description='List Helm releases (JSON metadata) using the local Helm CLI against the configured kubeconfig/context.',
    input_schema={'type': 'object', 'properties': {'all_namespaces': {'type': 'boolean', 'default': True, 'description': 'When true, list releases in all namespaces (-A)'}, 'namespace': {'type': 'string', 'default': '', 'description': 'When set (and all_namespaces is false), scope with -n'}, 'default_namespace': {'type': 'string', 'default': '', 'description': 'Fallback namespace when all_namespaces is false and namespace empty'}, 'max_releases': {'type': 'integer', 'default': 256, 'description': 'Cap for helm list --max (bounded by the client)'}, 'integration_id': {'type': 'string', 'default': '', 'description': 'Integration id'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('helm_path', 'kube_context', 'kubeconfig'),
    requires=['helm_path'],
    use_cases=['Finding which Helm release name/namespace to investigate for a failing workload', 'Correlating incident time with chart revisions across namespaces'],
)
def helm_list_releases(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.HelmTools',
            attr='helm_list_releases',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"helm_list_releases failed: {exc}"}
