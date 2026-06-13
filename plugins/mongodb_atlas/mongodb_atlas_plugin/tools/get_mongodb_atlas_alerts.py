"""Bridged tool: get_mongodb_atlas_alerts (from OpenSRE app.tools.MongoDBAtlasAlertsTool)."""

from __future__ import annotations

from typing import Any

from mongodb_atlas_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_mongodb_atlas_alerts',
    source='mongodb_atlas',
    description='Retrieve open alerts for a MongoDB Atlas project including event type, metric, cluster, and current value.',
    input_schema={'type': 'object', 'properties': {'api_public_key': {'type': 'string'}, 'api_private_key': {'type': 'string'}, 'base_url': {'type': 'string'}, 'max_results': {'type': 'integer'}}, 'required': ['api_public_key', 'api_private_key']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('project_id', 'public_key', 'private_key'),
    requires=[],
    use_cases=[],
)
def get_mongodb_atlas_alerts(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.MongoDBAtlasAlertsTool',
            attr='get_mongodb_atlas_alerts',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_mongodb_atlas_alerts failed: {exc}"}
