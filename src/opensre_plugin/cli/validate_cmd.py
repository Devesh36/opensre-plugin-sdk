"""``opensre-plugin validate`` command."""

from __future__ import annotations

from pathlib import Path

import click

from opensre_plugin.exceptions import ManifestError, OpensreNotInstalledError
from opensre_plugin.manifest import import_tools_package, load_manifest, validate_manifest
from opensre_plugin.schema.validator import iter_plugin_tools, validate_all_tools_in_module


def _known_evidence_sources() -> set[str] | None:
    try:
        from typing import get_args

        from app.types.evidence import EvidenceSource

        return set(get_args(EvidenceSource))
    except ImportError:
        return None


@click.command("validate")
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=".",
)
def validate(path: Path) -> None:
    """Validate plugin manifest and tool schemas offline."""
    errors: list[str] = []

    try:
        manifest = load_manifest(path)
    except ManifestError as exc:
        click.echo(f"ERROR: {exc}", err=True)
        raise SystemExit(1) from exc

    errors.extend(validate_manifest(manifest))

    try:
        tools_module = import_tools_package(manifest)
    except ImportError as exc:
        errors.append(f"tools_package {manifest.tools_package!r} import failed: {exc}")
        tools_module = None

    if tools_module is not None:
        errors.extend(validate_all_tools_in_module(tools_module))

        known_sources = _known_evidence_sources()
        if known_sources is not None:
            for tool_name, registered in iter_plugin_tools(tools_module):
                source = getattr(registered, "source", None)
                if isinstance(source, str) and source not in known_sources:
                    click.echo(
                        f"WARN: tool {tool_name!r} uses unknown source {source!r} "
                        "(may still work in Phase 1 MVP)",
                        err=True,
                    )

    if errors:
        click.echo(f"Validation failed for plugin {manifest.name!r}:", err=True)
        for error in errors:
            click.echo(f"  - {error}", err=True)
        raise SystemExit(1)

    tool_names = list_plugin_tool_names(tools_module) if tools_module else []
    click.echo(f"OK: plugin {manifest.name!r} ({len(tool_names)} tool(s))")
    for name in tool_names:
        click.echo(f"  - {name}")


def list_plugin_tool_names(tools_module: object) -> list[str]:
    from types import ModuleType

    from opensre_plugin.loader import list_plugin_tools

    if not isinstance(tools_module, ModuleType):
        return []
    return list_plugin_tools(tools_module)


@click.command("register")
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=".",
)
def register(path: Path) -> None:
    """Register plugin tools with OpenSRE (requires opensre installed)."""
    try:
        from opensre_plugin.loader import register_from_manifest
    except OpensreNotInstalledError as exc:
        click.echo(f"ERROR: {exc}", err=True)
        raise SystemExit(1) from exc

    try:
        manifest = load_manifest(path)
        register_from_manifest(path)
    except (ManifestError, OpensreNotInstalledError) as exc:
        click.echo(f"ERROR: {exc}", err=True)
        raise SystemExit(1) from exc
    except Exception as exc:
        click.echo(f"ERROR: {exc}", err=True)
        raise SystemExit(1) from exc

    tools_module = import_tools_package(manifest)
    for name in list_plugin_tool_names(tools_module):
        click.echo(f"Registered: {name}")
