#!/usr/bin/env python3
"""Export OpenSRE investigation tool metadata for plugin codegen."""

from __future__ import annotations

import importlib
import json
import pkgutil
from pathlib import Path
from typing import Any

from app import tools as tools_pkg
from app.tools.base import BaseTool
from app.tools.registered_tool import REGISTERED_TOOL_ATTR

OUTPUT = Path(__file__).resolve().parents[1] / "scripts" / ".tool_inventory.json"


def _tool_record(
    *,
    kind: str,
    name: str,
    source: str,
    module: str,
    attr: str,
    description: str,
    input_schema: dict[str, Any] | None,
    requires: list[str],
    use_cases: list[str],
) -> dict[str, Any]:
    return {
        "kind": kind,
        "name": name,
        "source": source,
        "module": module,
        "attr": attr,
        "description": description,
        "input_schema": input_schema,
        "requires": requires,
        "use_cases": use_cases,
    }


def main() -> int:
    tools: list[dict[str, Any]] = []
    for mod_name in sorted(m.name for m in pkgutil.iter_modules(tools_pkg.__path__)):
        if mod_name in {
            "base",
            "registry",
            "registered_tool",
            "tool_decorator",
            "investigation_registry",
            "utils",
        }:
            continue
        if mod_name.startswith("_"):
            continue
        mod = importlib.import_module(f"app.tools.{mod_name}")
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if isinstance(obj, BaseTool):
                tools.append(
                    _tool_record(
                        kind="base_tool",
                        name=obj.name,
                        source=obj.source,
                        module=mod.__name__,
                        attr=attr,
                        description=obj.description,
                        input_schema=obj.input_schema,
                        requires=list(obj.requires or []),
                        use_cases=list(obj.use_cases or []),
                    )
                )
                continue
            reg = getattr(obj, REGISTERED_TOOL_ATTR, None)
            if reg is not None and hasattr(reg, "name"):
                tools.append(
                    _tool_record(
                        kind="registered",
                        name=reg.name,
                        source=reg.source,
                        module=mod.__name__,
                        attr=attr,
                        description=getattr(reg, "description", ""),
                        input_schema=getattr(reg, "public_input_schema", None)
                        or getattr(reg, "input_schema", None),
                        requires=list(getattr(reg, "requires", []) or []),
                        use_cases=list(getattr(reg, "use_cases", []) or []),
                    )
                )

    OUTPUT.write_text(json.dumps(tools, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(tools)} tools to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
