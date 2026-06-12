"""Strict JSON Schema contract for investigation tool definitions.

Ports invariants from OpenSRE's ``tests/services/investigation_tool_schema_contract.py``.
Works without ``opensre`` installed.
"""

from __future__ import annotations

import importlib
import pkgutil
from types import ModuleType
from typing import Any, NoReturn

from opensre_plugin.schema.errors import SchemaValidationError

# Matches ``app.tools.registered_tool.REGISTERED_TOOL_ATTR`` for compatibility.
REGISTERED_TOOL_ATTR = "__opensre_registered_tool__"

# Keys stripped by the strictest investigation schema normalizer in OpenSRE today.
STRICT_UNSUPPORTED_SCHEMA_KEYS = frozenset(
    {
        "title",
        "$schema",
        "$defs",
        "definitions",
        "$ref",
        "not",
        "nullable",
    }
)


def _raise(*, tool_name: str, path: str, message: str) -> NoReturn:
    raise SchemaValidationError(tool_name=tool_name, path=path, message=message)


def _child_path(parent_path: str, segment: str) -> str:
    if not parent_path:
        return segment
    return f"{parent_path}.{segment}"


def assert_strict_tool_schema_node(
    node: Any,
    *,
    path: str,
    tool_name: str = "",
) -> None:
    """Enforce invariants strict LLM tool-schema APIs expect (string ``type``, typed arrays)."""
    if not isinstance(node, dict):
        return

    for key in node:
        if key in STRICT_UNSUPPORTED_SCHEMA_KEYS:
            _raise(
                tool_name=tool_name,
                path=_child_path(path, key),
                message=f"unsupported key {key!r}",
            )

    schema_type = node.get("type")
    if isinstance(schema_type, list):
        type_path = _child_path(path, "type") if path else "type"
        _raise(
            tool_name=tool_name,
            path=type_path,
            message=f"type must not be a list {schema_type!r}",
        )

    if "properties" in node:
        if schema_type != "object":
            _raise(
                tool_name=tool_name,
                path=_child_path(path, "properties"),
                message="properties without type object",
            )
        properties = node["properties"]
        if not isinstance(properties, dict):
            _raise(
                tool_name=tool_name,
                path=_child_path(path, "properties"),
                message="properties must be a dict",
            )
        properties_path = _child_path(path, "properties")
        for name, child in properties.items():
            assert_strict_tool_schema_node(
                child,
                path=_child_path(properties_path, name),
                tool_name=tool_name,
            )

    if schema_type == "array":
        items = node.get("items")
        if not isinstance(items, dict):
            _raise(tool_name=tool_name, path=path, message="array missing typed items")
        if "type" not in items and "properties" not in items:
            _raise(tool_name=tool_name, path=f"{path}[]", message="array items lack type")
        assert_strict_tool_schema_node(items, path=f"{path}[]", tool_name=tool_name)
    elif isinstance(node.get("items"), dict):
        assert_strict_tool_schema_node(node["items"], path=f"{path}[]", tool_name=tool_name)


def validate_tool_schema(schema: dict[str, Any] | None, *, tool_name: str = "") -> None:
    """Raise ``SchemaValidationError`` when *schema* violates strict invariants."""
    if schema is None:
        return

    if not isinstance(schema, dict):
        _raise(
            tool_name=tool_name,
            path=tool_name or "<root>",
            message="schema must be a dict",
        )

    if schema.get("type") != "object":
        _raise(
            tool_name=tool_name,
            path="<root>",
            message="top-level schema must have type 'object'",
        )

    properties = schema.get("properties")
    if not isinstance(properties, dict):
        _raise(
            tool_name=tool_name,
            path="<root>",
            message="top-level schema must have a properties dict",
        )

    assert_strict_tool_schema_node(schema, path="", tool_name=tool_name)


def _tool_schema_from_registered(tool: Any) -> dict[str, Any] | None:
    public_schema = getattr(tool, "public_input_schema", None)
    if isinstance(public_schema, dict):
        return public_schema
    input_schema = getattr(tool, "input_schema", None)
    if isinstance(input_schema, dict):
        return input_schema
    return None


def _tool_name_from_registered(tool: Any, fallback: str) -> str:
    name = getattr(tool, "name", None)
    if isinstance(name, str) and name:
        return name
    return fallback


def _iter_registered_tools(module: ModuleType) -> list[tuple[str, Any]]:
    tools: list[tuple[str, Any]] = []
    for attr_name in dir(module):
        obj = getattr(module, attr_name, None)
        registered = getattr(obj, REGISTERED_TOOL_ATTR, None)
        if registered is not None:
            tool_name = _tool_name_from_registered(registered, attr_name)
            tools.append((tool_name, registered))
    return tools


def _modules_to_scan(tools_module: ModuleType) -> tuple[list[ModuleType], list[str]]:
    modules: list[ModuleType] = [tools_module]
    import_errors: list[str] = []
    if hasattr(tools_module, "__path__"):
        prefix = tools_module.__name__ + "."
        for module_info in pkgutil.walk_packages(tools_module.__path__, prefix):
            try:
                modules.append(importlib.import_module(module_info.name))
            except ImportError as exc:
                import_errors.append(f"{module_info.name}: import failed: {exc}")
    return modules, import_errors


def iter_plugin_tools(tools_module: ModuleType) -> list[tuple[str, Any]]:
    """Return ``(tool_name, registered_tool)`` pairs from *tools_module* and submodules."""
    tools: list[tuple[str, Any]] = []
    modules, _ = _modules_to_scan(tools_module)
    for module in modules:
        tools.extend(_iter_registered_tools(module))
    return tools


def validate_all_tools_in_module(tools_module: ModuleType) -> list[str]:
    """Return validation error messages for every registered tool in *tools_module*."""
    errors: list[str] = []

    _, import_errors = _modules_to_scan(tools_module)
    errors.extend(import_errors)

    seen_names: set[str] = set()
    for tool_name, registered in iter_plugin_tools(tools_module):
        if tool_name in seen_names:
            errors.append(f"duplicate tool name {tool_name!r}")
        seen_names.add(tool_name)

        schema = _tool_schema_from_registered(registered)
        try:
            validate_tool_schema(schema, tool_name=tool_name)
        except SchemaValidationError as exc:
            errors.append(str(exc))

    return errors
