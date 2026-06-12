"""OpenSRE plugin SDK — external investigation tool plugins."""

from __future__ import annotations

from opensre_plugin.decorators import plugin_tool
from opensre_plugin.exceptions import (
    ManifestError,
    OpensreNotInstalledError,
    PluginRegistrationError,
)
from opensre_plugin.loader import (
    clear_and_register,
    list_plugin_tools,
    register_from_manifest,
    register_tools,
)
from opensre_plugin.manifest import PluginManifest, load_manifest, validate_manifest
from opensre_plugin.schema.errors import SchemaValidationError
from opensre_plugin.schema.validator import (
    assert_strict_tool_schema_node,
    validate_all_tools_in_module,
    validate_tool_schema,
)

__all__ = [
    "ManifestError",
    "OpensreNotInstalledError",
    "PluginManifest",
    "PluginRegistrationError",
    "SchemaValidationError",
    "assert_strict_tool_schema_node",
    "clear_and_register",
    "list_plugin_tools",
    "load_manifest",
    "plugin_tool",
    "register_from_manifest",
    "register_tools",
    "validate_all_tools_in_module",
    "validate_manifest",
    "validate_tool_schema",
]
