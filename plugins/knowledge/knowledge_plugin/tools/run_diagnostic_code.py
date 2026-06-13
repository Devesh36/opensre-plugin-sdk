"""Bridged tool: run_diagnostic_code (from OpenSRE app.tools.run_diagnostic_code)."""

from __future__ import annotations

from typing import Any

from knowledge_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='run_diagnostic_code',
    source='knowledge',
    description='Execute a Python snippet in a restricted sandbox for targeted diagnostics. Network access and filesystem writes outside /tmp/opensre are blocked. Execution is capped at 60 seconds. Use this to compute metrics, parse collected evidence, or run targeted analysis during investigations.',
    input_schema={'type': 'object', 'properties': {'code': {'type': 'string', 'description': 'Python source code to execute.'}, 'inputs': {'type': 'object', 'description': "Optional key-value pairs injected into the script's global scope as the 'inputs' variable."}, 'timeout': {'type': 'integer', 'description': 'Maximum execution time in seconds (default 30, max 60).'}}, 'required': ['code']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=[],
    use_cases=['parse or transform evidence already collected', 'compute statistics over collected metrics', 'run targeted analysis on log patterns', 'verify a hypothesis with lightweight calculation'],
)
def run_diagnostic_code(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.run_diagnostic_code',
            attr='run_diagnostic_code',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"run_diagnostic_code failed: {exc}"}
