"""Bridged tool: get_supabase_service_health (from OpenSRE app.tools.SupabaseHealthTool)."""

from __future__ import annotations

from typing import Any

from supabase_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_supabase_service_health',
    source='supabase',
    description='Check the health of all Supabase services (PostgREST, Auth, Storage) for a given project.',
    input_schema={'type': 'object', 'properties': {'project_url': {'type': 'string'}}, 'required': ['project_url']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'service_key'),
    requires=[],
    use_cases=['Checking Supabase project health during an incident', 'Identifying which Supabase service (Auth, Storage, PostgREST) is degraded', 'Triaging intermittent 503 or 401 errors from a Supabase-backed application'],
)
def get_supabase_service_health(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SupabaseHealthTool',
            attr='get_supabase_service_health',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_supabase_service_health failed: {exc}"}
