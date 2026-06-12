"""Integration tests for plugin loader (requires opensre)."""

from __future__ import annotations

import importlib
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from opensre_plugin.exceptions import PluginRegistrationError
from opensre_plugin.loader import clear_and_register, list_plugin_tools, register_tools
from opensre_plugin.schema.validator import REGISTERED_TOOL_ATTR

pytestmark = pytest.mark.integration

_INTEGRATION_PKG: ModuleType | None = None


def _integration_tools_package() -> ModuleType:
    global _INTEGRATION_PKG
    if _INTEGRATION_PKG is not None:
        return _INTEGRATION_PKG

    from app.tools.tool_decorator import tool

    _ = tool
    pkg_root = Path(__file__).parent / "fixtures" / "integration_plugin"
    pkg_root.mkdir(exist_ok=True)
    (pkg_root / "integration_plugin").mkdir(exist_ok=True)
    tools_dir = pkg_root / "integration_plugin" / "tools"
    tools_dir.mkdir(exist_ok=True)
    (tools_dir / "__init__.py").write_text("", encoding="utf-8")

    echo_path = tools_dir / "echo.py"
    echo_path.write_text(
        """
from __future__ import annotations

from typing import Any

from app.tools.tool_decorator import tool

@tool(
    name="integration_echo_tool",
    source="github",
    description="Integration test echo tool",
    input_schema={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
)
def integration_echo_tool(query: str) -> dict[str, Any]:
    return {"success": True, "query": query}
""",
        encoding="utf-8",
    )

    init_path = pkg_root / "integration_plugin" / "__init__.py"
    init_path.write_text('"""Integration plugin fixture."""\n', encoding="utf-8")

    import sys

    sys.path.insert(0, str(pkg_root))
    _INTEGRATION_PKG = importlib.import_module("integration_plugin.tools")
    return _INTEGRATION_PKG


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    from app.tools.registry import clear_tool_registry_cache

    clear_tool_registry_cache()
    yield
    clear_tool_registry_cache()


def test_register_valid_fixture_plugin() -> None:
    tools_pkg = _integration_tools_package()
    clear_and_register(tools_pkg)
    from app.tools.registry import get_registered_tools

    names = {tool.name for tool in get_registered_tools("investigation")}
    assert "integration_echo_tool" in names


def test_invalid_schema_raises_before_registry_mutation() -> None:
    import app.tools.registry as registry_module
    from app.tools.registry import get_registered_tools

    bad_module = ModuleType("invalid_plugin_tools")

    @dataclass(frozen=True)
    class BadTool:
        name: str
        public_input_schema: dict[str, Any]

    def bad_fn() -> dict[str, str]:
        return {"error": "unused"}

    setattr(
        bad_fn,
        REGISTERED_TOOL_ATTR,
        BadTool(
            name="bad_schema_tool",
            public_input_schema={
                "type": "object",
                "properties": {
                    "value": {"type": ["string", "null"]},
                },
            },
        ),
    )
    bad_module.bad_fn = bad_fn  # type: ignore[attr-defined]

    before = {tool.name for tool in get_registered_tools("investigation")}

    with pytest.raises(PluginRegistrationError, match="type must not be a list"):
        register_tools(bad_module)

    after = {tool.name for tool in get_registered_tools("investigation")}
    assert before == after
    assert bad_module not in registry_module._external_tool_packages


def test_double_registration_is_idempotent() -> None:
    import app.tools.registry as registry_module

    tools_pkg = _integration_tools_package()
    register_tools(tools_pkg)
    initial = registry_module._external_tool_packages.count(tools_pkg)
    register_tools(tools_pkg)
    assert registry_module._external_tool_packages.count(tools_pkg) == initial == 1


def test_concurrent_registration_is_thread_safe() -> None:
    import app.tools.registry as registry_module

    tools_pkg = _integration_tools_package()
    if tools_pkg in registry_module._external_tool_packages:
        registry_module._external_tool_packages.remove(tools_pkg)
        registry_module.clear_tool_registry_cache()

    barrier = threading.Barrier(parties=8)

    def attempt() -> None:
        barrier.wait()
        register_tools(tools_pkg)

    with ThreadPoolExecutor(max_workers=8) as pool:
        for future in [pool.submit(attempt) for _ in range(8)]:
            future.result()

    assert registry_module._external_tool_packages.count(tools_pkg) == 1


def test_list_plugin_tools_without_registering() -> None:
    import valid_plugin.tools as tools_pkg

    assert list_plugin_tools(tools_pkg) == ["fixture_echo_tool"]
