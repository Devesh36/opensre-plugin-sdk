"""Manifest parser tests."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

from opensre_plugin.exceptions import ManifestError
from opensre_plugin.manifest import PluginManifest, load_manifest, validate_manifest

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_valid_manifest() -> None:
    manifest = load_manifest(FIXTURES / "valid_plugin")
    assert manifest == PluginManifest(
        name="valid-fixture",
        tools_package="valid_plugin.tools",
        description="",
    )


def test_missing_required_name(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[tool.opensre-plugin]\ntools_package = "pkg.tools"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="name is required"):
        load_manifest(tmp_path)


def test_missing_opensre_plugin_table(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "demo"\n', encoding="utf-8")
    with pytest.raises(ManifestError, match="Missing \\[tool.opensre-plugin\\]"):
        load_manifest(tmp_path)


def test_invalid_toml(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("not = [valid", encoding="utf-8")
    with pytest.raises(tomllib.TOMLDecodeError):  # noqa: F821
        load_manifest(tmp_path)


def test_validate_manifest_import_error() -> None:
    manifest = PluginManifest(name="demo", tools_package="definitely.not.a.real.module")
    errors = validate_manifest(manifest)
    assert len(errors) == 1
    assert "not importable" in errors[0]
