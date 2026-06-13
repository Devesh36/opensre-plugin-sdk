"""Bridged tool: get_supabase_storage_buckets (from OpenSRE app.tools.SupabaseStorageTool)."""

from __future__ import annotations

from typing import Any

from supabase_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_supabase_storage_buckets',
    source='supabase',
    description='List all Supabase Storage buckets and their configuration metadata.',
    input_schema={'type': 'object', 'properties': {'project_url': {'type': 'string'}}, 'required': ['project_url']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('url', 'service_key'),
    requires=[],
    use_cases=['Auditing storage bucket configuration during a file upload incident', 'Checking whether a bucket is public or private when debugging access errors', 'Listing all buckets to identify orphaned or misconfigured storage resources'],
)
def get_supabase_storage_buckets(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.SupabaseStorageTool',
            attr='get_supabase_storage_buckets',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_supabase_storage_buckets failed: {exc}"}
