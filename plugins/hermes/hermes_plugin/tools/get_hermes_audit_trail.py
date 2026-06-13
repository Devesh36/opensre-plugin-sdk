"""Bridged tool: get_hermes_audit_trail (from OpenSRE app.tools.HermesSessionEvidenceTool)."""

from __future__ import annotations

from typing import Any

from hermes_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_hermes_audit_trail',
    source='hermes',
    description='Get Hermes audit policy and observed audit-chain/signature state.',
    input_schema={'type': 'object', 'properties': {'session_id': {'type': 'string'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=[],
    use_cases=['Diagnose missing cryptographic audit trails and broken hash chains'],
)
def get_hermes_audit_trail(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.HermesSessionEvidenceTool',
            attr='get_hermes_audit_trail',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_hermes_audit_trail failed: {exc}"}
