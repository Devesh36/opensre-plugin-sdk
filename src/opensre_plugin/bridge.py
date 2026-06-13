"""Delegate tool execution to OpenSRE core implementations (transitional bridge)."""

from __future__ import annotations

import importlib
from typing import Any

from opensre_plugin.exceptions import OpensreNotInstalledError


def delegate_to_opensre(*, module: str, attr: str, kwargs: dict[str, Any]) -> dict[str, Any]:
    """Call a BaseTool instance or @tool function from an OpenSRE module."""
    try:
        target_module = importlib.import_module(module)
    except ImportError as exc:
        raise OpensreNotInstalledError(f"running bridged tool {module}.{attr}") from exc

    target = getattr(target_module, attr, None)
    if target is None:
        return {"error": f"OpenSRE export {module}.{attr} not found"}

    try:
        from app.tools.base import BaseTool
    except ImportError as exc:
        raise OpensreNotInstalledError(f"running bridged tool {module}.{attr}") from exc

    if isinstance(target, BaseTool):
        result = target.run(**kwargs)
    elif callable(target):
        result = target(**kwargs)
    else:
        return {"error": f"{module}.{attr} is not a callable tool"}

    if not isinstance(result, dict):
        return {"success": True, "result": result}
    return result
