"""Bridged tool: get_mongodb_atlas_cluster_metrics (from OpenSRE app.tools.MongoDBAtlasMetricsTool)."""

from __future__ import annotations

from typing import Any

from mongodb_atlas_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mongodb_atlas_cluster_metrics',
    source='mongodb_atlas',
    description='Retrieve key process-level metrics for a MongoDB Atlas cluster including connections, opcounters, CPU, memory, cache, and disk IOPS.',
    input_schema={'type': 'object', 'properties': {'api_public_key': {'type': 'string'}, 'api_private_key': {'type': 'string'}, 'cluster_name': {'type': 'string'}, 'base_url': {'type': 'string'}, 'granularity': {'type': 'string'}, 'period': {'type': 'string'}}, 'required': ['api_public_key', 'api_private_key', 'cluster_name']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('project_id', 'public_key', 'private_key'),
    requires=[],
    use_cases=[],
)
def get_mongodb_atlas_cluster_metrics(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MongoDBAtlasMetricsTool',
            attr='get_mongodb_atlas_cluster_metrics',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mongodb_atlas_cluster_metrics failed: {exc}"}
