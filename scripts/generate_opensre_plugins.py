#!/usr/bin/env python3
"""Generate bridged plugin packages from OpenSRE tool inventory."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from integration_env import CREDENTIAL_PARAM_HINTS, NATIVE_PLUGINS, SOURCE_ENV

ROOT = Path(__file__).resolve().parents[1]
PLUGINS_DIR = ROOT / "plugins"
INVENTORY = Path(__file__).resolve().parent / ".tool_inventory.json"
BUNDLE_INIT = PLUGINS_DIR / "opensre_plugins" / "opensre_plugins" / "__init__.py"

SKIP_PLUGIN_DIRS = NATIVE_PLUGINS | {"opensre_plugins"}


def _slug_to_package(source: str) -> str:
    return f"{source}_plugin"


def _slug_to_distribution(source: str) -> str:
    return f"opensre-plugin-{source.replace('_', '-')}"


STRICT_UNSUPPORTED_SCHEMA_KEYS = frozenset(
    {"title", "$schema", "$defs", "definitions", "$ref", "not", "nullable"}
)


def _strip_unsupported_schema_keys(node: Any) -> Any:
    if isinstance(node, dict):
        return {
            key: _strip_unsupported_schema_keys(value)
            for key, value in node.items()
            if key not in STRICT_UNSUPPORTED_SCHEMA_KEYS
        }
    if isinstance(node, list):
        return [_strip_unsupported_schema_keys(item) for item in node]
    return node


def _normalize_schema_node(node: Any) -> Any:
    if isinstance(node, dict):
        normalized = {key: _normalize_schema_node(value) for key, value in node.items()}
        schema_type = normalized.get("type")
        if isinstance(schema_type, list):
            picked = next((t for t in schema_type if t != "null"), schema_type[0])
            normalized["type"] = picked
        if normalized.get("type") == "array" and "items" not in normalized:
            normalized["items"] = {"type": "string"}
        return normalized
    if isinstance(node, list):
        return [_normalize_schema_node(item) for item in node]
    return node


def _sanitize_schema(
    schema: dict[str, Any] | None,
    injected: tuple[str, ...],
) -> dict[str, Any] | None:
    if not schema:
        return None
    out = _normalize_schema_node(_strip_unsupported_schema_keys(json.loads(json.dumps(schema))))
    if not isinstance(out, dict):
        return None
    props = out.get("properties")
    if isinstance(props, dict):
        for key in injected:
            props.pop(key, None)
    required = out.get("required")
    if isinstance(required, list):
        out["required"] = [r for r in required if r not in injected]
        if not out["required"]:
            out.pop("required", None)
    return out


def _detect_injected(
    source: str,
    tool: dict[str, Any],
) -> tuple[str, ...]:
    env_cfg = SOURCE_ENV.get(source, {})
    inject_map = env_cfg.get("inject", {})
    if not isinstance(inject_map, dict):
        inject_map = {}

    candidates: list[str] = []
    schema = tool.get("input_schema") or {}
    props = schema.get("properties", {}) if isinstance(schema, dict) else {}
    if isinstance(props, dict):
        for name in props:
            if name in inject_map or name in CREDENTIAL_PARAM_HINTS:
                candidates.append(name)
    for req in tool.get("requires", []):
        if (req in inject_map or req in CREDENTIAL_PARAM_HINTS) and req not in candidates:
            candidates.append(req)

    for name in inject_map:
        if name not in candidates:
            candidates.append(name)
    return tuple(dict.fromkeys(candidates))


def _py_literal(value: Any) -> str:
    return repr(value)


def _render_config(source: str) -> str:
    env_cfg = SOURCE_ENV.get(source, {"gate": [], "inject": {}})
    gate = env_cfg.get("gate", [])
    inject = env_cfg.get("inject", {})
    if not isinstance(gate, list):
        gate = []
    if not isinstance(inject, dict):
        inject = {}

    gate_repr = repr(list(gate))
    inject_repr = _py_literal(inject)

    return f'''"""Environment configuration for the {source} integration (Phase 1)."""

from __future__ import annotations

import os
from typing import Any

GATE_ENV_VARS: tuple[str, ...] = {gate_repr}

INJECT_ENV_MAP: dict[str, str] = {inject_repr}


def is_configured() -> bool:
    if not GATE_ENV_VARS:
        return True
    return any(os.environ.get(name, "").strip() for name in GATE_ENV_VARS)


def extract_env_params() -> dict[str, Any]:
    return {{
        param: os.environ.get(env_name, "")
        for param, env_name in INJECT_ENV_MAP.items()
    }}


def _available(sources: dict[str, dict]) -> bool:
    _ = sources
    return is_configured()


def _extract_params(sources: dict[str, dict]) -> dict[str, Any]:
    _ = sources
    return extract_env_params()
'''


def _render_tool_module(source: str, tool: dict[str, Any], injected: tuple[str, ...]) -> str:
    pkg = _slug_to_package(source)
    schema = _sanitize_schema(tool.get("input_schema"), injected)
    schema_block = "None" if schema is None else _py_literal(schema)
    use_cases = tool.get("use_cases") or []
    requires = list(tool.get("requires") or [])
    injected_block = repr(injected) if injected else "()"
    description = tool["description"].replace('"""', '\\"\\"\\"')

    body = f'''"""Bridged tool: {tool["name"]} (from OpenSRE {tool["module"]})."""

from __future__ import annotations

from typing import Any

from {pkg}.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name={tool["name"]!r},
    source={tool["source"]!r},
    description={description!r},
    input_schema={schema_block},
    is_available=_available,
    extract_params=_extract_params,
    injected_params={injected_block},
    requires={requires!r},
    use_cases={use_cases!r},
)
def {tool["name"]}(**kwargs: Any) -> dict[str, Any]:
    payload = {{**_extract_params({{}}), **kwargs}}
    try:
        return delegate_to_opensre(
            module={tool["module"]!r},
            attr={tool["attr"]!r},
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {{"error": str(exc)}}
        return {{"error": f"{tool["name"]} failed: {{exc}}"}}
'''
    return body


def _render_pyproject(source: str, tool_count: int) -> str:
    dist = _slug_to_distribution(source)
    pkg = _slug_to_package(source)
    return f'''[project]
name = "{dist}"
version = "0.1.0"
description = "OpenSRE {source} integration plugin ({tool_count} tool(s), bridged from core)"
requires-python = ">=3.12"
dependencies = [
    "opensre-plugin-sdk",
]

[project.optional-dependencies]
opensre = ["opensre>=0.1"]

[tool.opensre-plugin]
name = "{source}"
tools_package = "{pkg}.tools"
description = "Bridged {source} tools for OpenSRE investigations"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{pkg}"]
'''


def _render_init(source: str) -> str:
    pkg = _slug_to_package(source)
    return f'''"""{source} plugin — bridged from OpenSRE core tools."""

from __future__ import annotations


def register() -> None:
    from {pkg} import tools
    from opensre_plugin.loader import register_tools

    register_tools(tools)
'''


def _render_readme(source: str, tools: list[dict[str, Any]]) -> str:
    env_cfg = SOURCE_ENV.get(source, {})
    gate = env_cfg.get("gate", [])
    lines = [
        f"# {_slug_to_distribution(source)}",
        "",
        f"Bridged OpenSRE **{source}** integration ({len(tools)} tool(s)).",
        "Tool implementations delegate to `opensre` core until fully ported.",
        "",
        "## Env vars",
        "",
    ]
    if gate:
        for var in gate:
            lines.append(f"- `{var}`")
    else:
        lines.append("- No credentials required")
    lines.extend(["", "## Tools", ""])
    for tool in sorted(tools, key=lambda t: t["name"]):
        lines.append(f"- `{tool['name']}`")
    lines.extend(
        [
            "",
            "## Install",
            "",
            "```bash",
            f"pip install -e plugins/{source}",
            "pip install opensre  # required for bridged tool execution",
            "```",
            "",
            "## Validate",
            "",
            "```bash",
            f"opensre-plugin validate plugins/{source}",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_bundle_init(sources: list[str]) -> None:
    registrars = {src: f"{_slug_to_package(src)}:register" for src in sorted(sources)}
    registrars.update({"linear": "linear_plugin:register", "mock": "mock_plugin:register"})
    lines = [
        '"""Register bundled OpenSRE integration plugins from one entry point."""',
        "",
        "from __future__ import annotations",
        "",
        "from collections.abc import Callable",
        "from importlib import import_module",
        "",
        "PLUGIN_REGISTRARS: dict[str, str] = {",
    ]
    for name, entry in sorted(registrars.items()):
        lines.append(f'    "{name}": "{entry}",')
    lines.extend(
        [
            "}",
            "",
            "",
            "def list_plugins() -> list[str]:",
            '    """Return names of plugins known to this bundle."""',
            "    return sorted(PLUGIN_REGISTRARS)",
            "",
            "",
            "def _resolve_register(entry: str) -> Callable[[], None]:",
            '    module_path, func_name = entry.split(":", 1)',
            "    module = import_module(module_path)",
            "    register = getattr(module, func_name, None)",
            '    if register is None or not callable(register):',
            '        raise TypeError(f"{entry!r} is not a callable register() entry point")',
            "    return register",
            "",
            "",
            "def register_all(",
            "    *,",
            "    only: list[str] | None = None,",
            "    skip_missing: bool = True,",
            ") -> list[str]:",
            '    """Register every installed plugin in this bundle.',
            "",
            "    Returns the plugin names that were registered successfully.",
            "    Skips plugins that are not installed when *skip_missing* is True.",
            '    """',
            "    registered: list[str] = []",
            "    for name, entry in PLUGIN_REGISTRARS.items():",
            "        if only is not None and name not in only:",
            "            continue",
            "        try:",
            "            _resolve_register(entry)()",
            "        except ImportError:",
            "            if not skip_missing:",
            "                raise",
            "            continue",
            "        registered.append(name)",
            "    return registered",
            "",
        ]
    )
    BUNDLE_INIT.write_text("\n".join(lines), encoding="utf-8")


def _update_workspace_members(sources: list[str]) -> None:
    pyproject = ROOT / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    members = ['    "plugins/linear"', '    "plugins/mock"', '    "plugins/opensre_plugins"']
    for source in sorted(sources):
        members.append(f'    "plugins/{source}"')
    workspace = "[tool.uv.workspace]\nmembers = [\n" + ",\n".join(members) + "\n]\n"

    sources_lines = ["[tool.uv.sources]", "opensre-plugin-sdk = { workspace = true }"]
    for source in sorted(set(sources) | {"linear", "mock"}):
        dist = _slug_to_distribution(source)
        sources_lines.append(f"{dist} = {{ workspace = true }}")
    sources_lines.append("opensre-plugins = { workspace = true }")
    sources_section = "\n".join(sources_lines) + "\n"

    if "[tool.uv.workspace]" not in text:
        text = text.rstrip() + "\n\n" + workspace + "\n" + sources_section
    else:
        text = re.sub(
            r"\[tool\.uv\.workspace\]\nmembers = \[.*?\]\n",
            workspace,
            text,
            count=1,
            flags=re.DOTALL,
        )
        text = re.sub(
            r"\[tool\.uv\.sources\]\n.*?(?=\n\[tool\.pytest|\n\[tool\.ruff|\Z)",
            sources_section,
            text,
            count=1,
            flags=re.DOTALL,
        )
    pyproject.write_text(text, encoding="utf-8")


def generate() -> int:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for tool in inventory:
        by_source[tool["source"]].append(tool)

    generated_sources: list[str] = []
    for source in sorted(by_source):
        if source in SKIP_PLUGIN_DIRS:
            continue
        tools = by_source[source]
        plugin_dir = PLUGINS_DIR / source
        pkg = _slug_to_package(source)
        pkg_dir = plugin_dir / pkg
        tools_dir = pkg_dir / "tools"

        tools_dir.mkdir(parents=True, exist_ok=True)
        (pkg_dir / "__init__.py").write_text(_render_init(source), encoding="utf-8")
        (pkg_dir / "config.py").write_text(_render_config(source), encoding="utf-8")
        tools_init = '"""Tool modules for this plugin."""\n'
        (tools_dir / "__init__.py").write_text(tools_init, encoding="utf-8")
        (plugin_dir / "pyproject.toml").write_text(
            _render_pyproject(source, len(tools)), encoding="utf-8"
        )
        (plugin_dir / "README.md").write_text(_render_readme(source, tools), encoding="utf-8")

        for tool in tools:
            injected = _detect_injected(source, tool)
            safe_name = re.sub(r"[^a-z0-9_]+", "_", tool["name"].lower())
            (tools_dir / f"{safe_name}.py").write_text(
                _render_tool_module(source, tool, injected),
                encoding="utf-8",
            )

        generated_sources.append(source)
        print(f"generated plugins/{source} ({len(tools)} tools)")

    _write_bundle_init(generated_sources)
    _update_workspace_members(generated_sources)
    print(f"Done: {len(generated_sources)} bridge plugins + linear + mock")
    return 0


if __name__ == "__main__":
    raise SystemExit(generate())
