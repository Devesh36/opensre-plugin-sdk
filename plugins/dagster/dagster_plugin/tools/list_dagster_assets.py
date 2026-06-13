"""Bridged tool: list_dagster_assets (from OpenSRE app.tools.DagsterAssetsTool)."""

from __future__ import annotations

from typing import Any

from dagster_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='list_dagster_assets',
    source='dagster',
    description='List Dagster assets and their latest materialization status.',
    input_schema={'type': 'object', 'properties': {'limit': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('endpoint', 'api_token'),
    requires=[],
    use_cases=[],
)
def list_dagster_assets(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.DagsterAssetsTool',
            attr='list_dagster_assets',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"list_dagster_assets failed: {exc}"}
