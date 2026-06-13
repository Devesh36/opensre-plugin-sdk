"""Bridged tool: get_hermes_logs (from OpenSRE app.tools.HermesLogsTool)."""

from __future__ import annotations

from typing import Any

from hermes_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_hermes_logs',
    source='hermes',
    description="Read Hermes Agent's own ~/.hermes/logs/errors.log (or another Hermes log file) incrementally. Use op='scan' for a one-shot read of the last N records or op='tail' for cursor-driven incremental polling that only returns lines new since the previous call. Records are parsed and any incidents the classifier would emit on this window are included.",
    input_schema={'type': 'object', 'properties': {'op': {'type': 'string', 'enum': ['scan', 'tail'], 'default': 'scan', 'description': "'scan' for a one-shot read; 'tail' for cursor-driven incremental polling."}, 'log_path': {'type': 'string', 'description': 'Path to the Hermes log file. Defaults to $HERMES_LOG_PATH or ~/.hermes/logs/errors.log.'}, 'cursor': {'type': 'string', 'description': "Opaque resume token returned by a previous call. Required for op='tail' on the second+ call. Ignored for op='scan'."}, 'tail_lines': {'type': 'integer', 'default': 200, 'minimum': 1, 'maximum': 200, 'description': "For op='scan': how many recent records to return. Ignored for op='tail'."}, 'max_records': {'type': 'integer', 'default': 200, 'minimum': 1, 'maximum': 200, 'description': 'Upper bound on records included in the response. Hits truncated_response_records when exceeded.'}, 'levels': {'type': 'array', 'items': {'type': 'string', 'enum': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']}, 'description': 'Only return records at these levels. The classifier still observes filtered records so traceback continuations and warning-burst windows remain accurate.'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=(),
    requires=[],
    use_cases=['Investigating why the agent itself is failing (gateway crashes, auth bypass, polling conflicts)', 'Following a Hermes log live during an active incident without re-reading the entire file on every call', 'Surfacing structured incidents (error_severity, traceback, warning_burst) from a slice of recent log activity'],
)
def get_hermes_logs(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.HermesLogsTool',
            attr='get_hermes_logs',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_hermes_logs failed: {exc}"}
