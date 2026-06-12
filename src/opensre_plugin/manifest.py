"""Parse ``[tool.opensre-plugin]`` manifest from ``pyproject.toml``."""

from __future__ import annotations

import importlib
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from opensre_plugin.exceptions import ManifestError


@dataclass(frozen=True)
class PluginManifest:
    name: str
    tools_package: str
    root_dir: Path
    description: str = ""


_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*$")


def _find_pyproject(start: Path) -> Path:
    path = start.resolve()
    if path.is_file() and path.name == "pyproject.toml":
        return path
    if path.is_dir():
        candidate = path / "pyproject.toml"
        if candidate.is_file():
            return candidate
    raise ManifestError(f"pyproject.toml not found under {start}")


def load_manifest(path: Path | None = None) -> PluginManifest:
    """Load ``[tool.opensre-plugin]`` from ``pyproject.toml`` in *path* or cwd."""
    base = path or Path.cwd()
    pyproject_path = _find_pyproject(base)
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    section = data.get("tool", {}).get("opensre-plugin")
    if not isinstance(section, dict):
        raise ManifestError(
            f"Missing [tool.opensre-plugin] table in {pyproject_path}. "
            "Add name and tools_package fields."
        )

    name = section.get("name")
    tools_package = section.get("tools_package")
    if not isinstance(name, str) or not name.strip():
        raise ManifestError("[tool.opensre-plugin].name is required")
    if not isinstance(tools_package, str) or not tools_package.strip():
        raise ManifestError("[tool.opensre-plugin].tools_package is required")

    description = section.get("description", "")
    if description is None:
        description = ""
    if not isinstance(description, str):
        raise ManifestError("[tool.opensre-plugin].description must be a string")

    return PluginManifest(
        name=name.strip(),
        tools_package=tools_package.strip(),
        root_dir=pyproject_path.parent,
        description=description.strip(),
    )


def ensure_plugin_root_on_path(manifest: PluginManifest) -> None:
    """Insert *manifest.root_dir* on ``sys.path`` so local plugins import without install."""
    import sys

    root = str(manifest.root_dir.resolve())
    if root not in sys.path:
        sys.path.insert(0, root)


def import_tools_package(manifest: PluginManifest) -> ModuleType:
    """Import *manifest.tools_package* after ensuring *root_dir* is on ``sys.path``."""
    ensure_plugin_root_on_path(manifest)
    return importlib.import_module(manifest.tools_package)


def validate_manifest(manifest: PluginManifest) -> list[str]:
    """Check manifest fields and that *tools_package* is importable."""
    errors: list[str] = []

    if not _NAME_PATTERN.match(manifest.name):
        errors.append(
            f"plugin name {manifest.name!r} must match {_NAME_PATTERN.pattern} "
            "(lowercase identifier)"
        )

    try:
        import_tools_package(manifest)
    except ImportError as exc:
        errors.append(f"tools_package {manifest.tools_package!r} is not importable: {exc}")

    return errors
