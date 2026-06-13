"""Bridged tool: helm_release_history (from OpenSRE app.tools.HelmTools)."""

from __future__ import annotations

from typing import Any

from helm_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='helm_release_history',
    source='helm',
    description='Fetch Helm revision history (status, chart version, description per revision).',
    input_schema={'type': 'object', 'properties': {'release_name': {'type': 'string'}, 'namespace': {'type': 'string', 'default': ''}, 'default_namespace': {'type': 'string', 'default': ''}, 'max_revisions': {'type': 'integer', 'default': 10}, 'integration_id': {'type': 'string', 'default': ''}}, 'required': ['release_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('helm_path', 'kube_context', 'kubeconfig'),
    requires=['release_name'],
    use_cases=['Seeing recent failed rollouts or rollbacks for a Helm release', 'Comparing chart versions between revisions during an incident window'],
)
def helm_release_history(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.HelmTools',
            attr='helm_release_history',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"helm_release_history failed: {exc}"}
