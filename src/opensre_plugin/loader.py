"""Register validated external tool packages with OpenSRE."""

from __future__ import annotations

import importlib
import threading
from pathlib import Path
from types import ModuleType

from opensre_plugin.exceptions import OpensreNotInstalledError, PluginRegistrationError
from opensre_plugin.manifest import load_manifest
from opensre_plugin.schema.validator import iter_plugin_tools, validate_all_tools_in_module

_registration_lock = threading.Lock()
_registered_packages: set[str] = set()


def _require_opensre() -> None:
    try:
        import app.tools.registry  # noqa: F401
    except ImportError as exc:
        raise OpensreNotInstalledError("registering tools with OpenSRE") from exc


def list_plugin_tools(tools_package: ModuleType) -> list[str]:
    """Return tool names defined in *tools_package* without registering."""
    names = [name for name, _ in iter_plugin_tools(tools_package)]
    return sorted(set(names))


def register_tools(tools_package: ModuleType) -> None:
    """Validate tool schemas and register *tools_package* with OpenSRE."""
    _require_opensre()
    from app.tools.registry import get_registered_tools, register_external_tool_package

    errors = validate_all_tools_in_module(tools_package)
    if errors:
        raise PluginRegistrationError("\n".join(errors))

    expected_names = list_plugin_tools(tools_package)
    if not expected_names:
        raise PluginRegistrationError(
            f"No tools found in package {tools_package.__name__!r}. "
            "Ensure tools are decorated with @plugin_tool or @tool."
        )

    with _registration_lock:
        register_external_tool_package(tools_package)
        _registered_packages.add(tools_package.__name__)

    registered_names = {tool.name for tool in get_registered_tools("investigation")}
    missing = [name for name in expected_names if name not in registered_names]
    if missing:
        raise PluginRegistrationError(
            f"Tools registered in package {tools_package.__name__!r} did not appear "
            f"in investigation registry: {', '.join(missing)}"
        )


def register_from_manifest(manifest_path: Path | None = None) -> None:
    """Load ``[tool.opensre-plugin]`` from ``pyproject.toml`` and register tools."""
    manifest = load_manifest(manifest_path)
    tools_package = importlib.import_module(manifest.tools_package)
    register_tools(tools_package)


def clear_and_register(tools_package: ModuleType) -> None:
    """For tests: clear OpenSRE tool registry cache then register *tools_package*."""
    _require_opensre()
    from app.tools.registry import clear_tool_registry_cache

    with _registration_lock:
        clear_tool_registry_cache()
        _registered_packages.discard(tools_package.__name__)
    register_tools(tools_package)
