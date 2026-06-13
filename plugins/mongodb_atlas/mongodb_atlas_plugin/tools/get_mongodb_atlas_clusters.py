"""Bridged tool: get_mongodb_atlas_clusters (from OpenSRE app.tools.MongoDBAtlasClustersTool)."""

from __future__ import annotations

from typing import Any

from mongodb_atlas_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mongodb_atlas_clusters',
    source='mongodb_atlas',
    description='Retrieve all MongoDB Atlas clusters in a project including state, version, instance size, and replication topology.',
    input_schema={'type': 'object', 'properties': {'api_public_key': {'type': 'string'}, 'api_private_key': {'type': 'string'}, 'base_url': {'type': 'string'}}, 'required': ['api_public_key', 'api_private_key']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('project_id', 'public_key', 'private_key'),
    requires=[],
    use_cases=[],
)
def get_mongodb_atlas_clusters(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MongoDBAtlasClustersTool',
            attr='get_mongodb_atlas_clusters',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mongodb_atlas_clusters failed: {exc}"}
