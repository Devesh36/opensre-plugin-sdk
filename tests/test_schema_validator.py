"""Tests for strict investigation tool schema validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from opensre_plugin.schema.errors import SchemaValidationError
from opensre_plugin.schema.validator import (
    REGISTERED_TOOL_ATTR,
    assert_strict_tool_schema_node,
    validate_all_tools_in_module,
    validate_tool_schema,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


class TestValidateToolSchema:
    def test_valid_minimal_object_schema(self) -> None:
        schema = _load_json(FIXTURES / "valid_schema.json")
        validate_tool_schema(schema, tool_name="search_issues")

    def test_valid_nested_object(self) -> None:
        schema = {
            "type": "object",
            "properties": {
                "filter": {
                    "type": "object",
                    "properties": {
                        "service": {"type": "string"},
                        "severity": {"type": "string"},
                    },
                    "required": ["service"],
                }
            },
            "required": ["filter"],
        }
        validate_tool_schema(schema, tool_name="nested_tool")

    def test_valid_array_with_typed_items(self) -> None:
        schema = {
            "type": "object",
            "properties": {
                "ids": {
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
            "required": ["ids"],
        }
        validate_tool_schema(schema, tool_name="array_tool")

    def test_valid_array_with_object_items(self) -> None:
        schema = {
            "type": "object",
            "properties": {
                "entries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"key": {"type": "string"}},
                        "required": ["key"],
                    },
                }
            },
            "required": ["entries"],
        }
        validate_tool_schema(schema, tool_name="object_array_tool")

    def test_none_schema_passes(self) -> None:
        validate_tool_schema(None, tool_name="implicit_schema_tool")

    def test_type_union_at_top_level_properties(self) -> None:
        schema = _load_json(FIXTURES / "invalid_schemas/type_union.json")
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="query_eks_logs")
        assert exc_info.value.tool_name == "query_eks_logs"
        assert exc_info.value.path == "properties.credentials.type"
        assert "type must not be a list" in exc_info.value.message

    def test_array_missing_items(self) -> None:
        schema = _load_json(FIXTURES / "invalid_schemas/array_no_items.json")
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="tag_tool")
        assert exc_info.value.path == "properties.tags"
        assert "array missing typed items" in exc_info.value.message

    def test_array_items_empty_object(self) -> None:
        schema = {
            "type": "object",
            "properties": {
                "values": {
                    "type": "array",
                    "items": {},
                }
            },
        }
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="empty_items")
        assert exc_info.value.path == "properties.values[]"
        assert "array items lack type" in exc_info.value.message

    def test_ref_key_rejected(self) -> None:
        schema = {
            "type": "object",
            "properties": {
                "payload": {"$ref": "#/definitions/Foo"},
            },
        }
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="ref_tool")
        assert "unsupported key '$ref'" in exc_info.value.message

    def test_nullable_key_rejected(self) -> None:
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "nullable": True},
            },
        }
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="nullable_tool")
        assert exc_info.value.path == "properties.name.nullable"
        assert "unsupported key 'nullable'" in exc_info.value.message

    def test_title_key_rejected(self) -> None:
        schema = {
            "type": "object",
            "title": "MyTool",
            "properties": {"q": {"type": "string"}},
        }
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="title_tool")
        assert exc_info.value.path == "title"
        assert "unsupported key 'title'" in exc_info.value.message

    def test_schema_key_rejected(self) -> None:
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {"q": {"type": "string"}},
        }
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="draft_tool")
        assert "unsupported key '$schema'" in exc_info.value.message

    def test_deeply_nested_invalid_node_reports_path(self) -> None:
        schema = {
            "type": "object",
            "properties": {
                "outer": {
                    "type": "object",
                    "properties": {
                        "inner": {
                            "type": "array",
                            "items": {"type": ["string", "null"]},
                        }
                    },
                }
            },
        }
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="deep_tool")
        assert exc_info.value.path == "properties.outer.properties.inner[].type"
        assert "type must not be a list" in exc_info.value.message

    def test_properties_without_type_object(self) -> None:
        schema = {
            "type": "string",
            "properties": {"q": {"type": "string"}},
        }
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="bad_root")
        assert "top-level schema must have type 'object'" in exc_info.value.message

    def test_missing_properties_dict(self) -> None:
        schema = {"type": "object"}
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_tool_schema(schema, tool_name="no_props")
        assert "top-level schema must have a properties dict" in exc_info.value.message

    def test_error_str_format(self) -> None:
        err = SchemaValidationError(
            tool_name="query_eks_logs",
            path="properties.credentials.type",
            message="type must not be a list ['object', 'null']",
        )
        assert str(err) == (
            "tool 'query_eks_logs' at 'properties.credentials.type': "
            "type must not be a list ['object', 'null']"
        )


class TestAssertStrictToolSchemaNode:
    def test_non_dict_node_is_noop(self) -> None:
        assert_strict_tool_schema_node("string", path="root", tool_name="t")

    def test_nested_type_union_via_assert(self) -> None:
        node = {
            "type": "object",
            "properties": {
                "flag": {"type": ["boolean", "null"]},
            },
        }
        with pytest.raises(SchemaValidationError) as exc_info:
            assert_strict_tool_schema_node(node, path="", tool_name="my_tool")
        assert exc_info.value.path == "properties.flag.type"


@dataclass(frozen=True)
class _FakeRegisteredTool:
    name: str
    public_input_schema: dict[str, Any] | None


def _attach_tool(module: ModuleType, tool: _FakeRegisteredTool, attr: str) -> None:
    def stub() -> None:
        pass

    setattr(stub, REGISTERED_TOOL_ATTR, tool)
    setattr(module, attr, stub)


class TestValidateAllToolsInModule:
    def test_valid_tools_return_no_errors(self) -> None:
        module = ModuleType("fake_tools_valid")
        _attach_tool(
            module,
            _FakeRegisteredTool(
                name="tool_a",
                public_input_schema=_load_json(FIXTURES / "valid_schema.json"),
            ),
            "tool_a_fn",
        )
        assert validate_all_tools_in_module(module) == []

    def test_invalid_tool_returns_error_message(self) -> None:
        module = ModuleType("fake_tools_invalid")
        _attach_tool(
            module,
            _FakeRegisteredTool(
                name="bad_tool",
                public_input_schema=_load_json(FIXTURES / "invalid_schemas/type_union.json"),
            ),
            "bad_tool_fn",
        )
        errors = validate_all_tools_in_module(module)
        assert len(errors) == 1
        assert "bad_tool" in errors[0]
        assert "type must not be a list" in errors[0]

    def test_duplicate_tool_names_reported(self) -> None:
        module = ModuleType("fake_tools_dup")
        schema = _load_json(FIXTURES / "valid_schema.json")
        _attach_tool(module, _FakeRegisteredTool(name="dup", public_input_schema=schema), "fn1")
        _attach_tool(module, _FakeRegisteredTool(name="dup", public_input_schema=schema), "fn2")
        errors = validate_all_tools_in_module(module)
        assert any("duplicate tool name 'dup'" in err for err in errors)

    def test_falls_back_to_input_schema(self) -> None:
        module = ModuleType("fake_tools_input_schema")

        @dataclass(frozen=True)
        class ToolWithInputSchema:
            name: str
            input_schema: dict[str, Any]

        _attach_tool(
            module,
            ToolWithInputSchema(
                name="legacy",
                input_schema=_load_json(FIXTURES / "valid_schema.json"),
            ),
            "legacy_fn",
        )
        assert validate_all_tools_in_module(module) == []
