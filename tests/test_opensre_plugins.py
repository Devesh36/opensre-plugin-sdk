"""Tests for the opensre_plugins bundle."""

from __future__ import annotations

import sys
from contextlib import suppress
from importlib import import_module
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = ROOT / "plugins" / "opensre_plugins"
LINEAR_ROOT = ROOT / "plugins" / "linear"
MOCK_ROOT = ROOT / "plugins" / "mock"


@pytest.fixture(autouse=True)
def bundle_importable() -> None:
    for path in (BUNDLE_ROOT, LINEAR_ROOT, MOCK_ROOT):
        sys.path.insert(0, str(path))
    yield
    for path in (BUNDLE_ROOT, LINEAR_ROOT, MOCK_ROOT):
        with suppress(ValueError):
            sys.path.remove(str(path))


def test_list_plugins() -> None:
    from opensre_plugins import list_plugins

    names = list_plugins()
    assert "linear" in names
    assert "mock" in names
    assert "vercel" in names
    assert "datadog" in names
    assert len(names) == 53


def test_plugin_register_entry_points_are_importable() -> None:
    from opensre_plugins import PLUGIN_REGISTRARS

    for entry in PLUGIN_REGISTRARS.values():
        module_path, func_name = entry.split(":", 1)
        module = import_module(module_path)
        register = getattr(module, func_name, None)
        assert callable(register)


@pytest.mark.integration
def test_register_all_with_opensre() -> None:
    pytest.importorskip("app.tools.registry")
    from app.tools.registry import clear_tool_registry_cache
    from opensre_plugins import register_all

    clear_tool_registry_cache()
    registered = register_all(only=["mock"])
    assert registered == ["mock"]
