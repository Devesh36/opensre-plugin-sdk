"""``@plugin_tool`` decorator — validated wrapper over OpenSRE's ``@tool``."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast, overload

from opensre_plugin.schema.validator import REGISTERED_TOOL_ATTR, validate_tool_schema


@dataclass(frozen=True)
class _OfflineToolStub:
    """Minimal tool metadata for offline ``opensre-plugin validate`` without OpenSRE."""

    name: str
    source: str
    public_input_schema: dict[str, Any] | None


def _opensre_tool() -> Any | None:
    try:
        from app.tools.tool_decorator import tool
    except ImportError:
        return None
    return tool


def _attach_offline_stub[F: Callable[..., Any]](
    func: F,
    *,
    name: str,
    source: str,
    input_schema: dict[str, Any] | None,
) -> F:
    setattr(
        func,
        REGISTERED_TOOL_ATTR,
        _OfflineToolStub(name=name, source=source, public_input_schema=input_schema),
    )
    return func


@overload
def plugin_tool(
    func: Any,
    *,
    name: str,
    source: str,
    description: str,
    input_schema: dict[str, Any] | None = None,
    is_available: Callable[[dict[str, dict[str, Any]]], bool] | None = None,
    extract_params: Callable[[dict[str, dict[str, Any]]], dict[str, Any]] | None = None,
    surfaces: tuple[str, ...] = ("investigation",),
    injected_params: tuple[str, ...] | None = None,
    requires: list[str] | None = None,
    use_cases: list[str] | None = None,
    **kwargs: Any,
) -> Any: ...


@overload
def plugin_tool(
    *,
    name: str,
    source: str,
    description: str,
    input_schema: dict[str, Any] | None = None,
    is_available: Callable[[dict[str, dict[str, Any]]], bool] | None = None,
    extract_params: Callable[[dict[str, dict[str, Any]]], dict[str, Any]] | None = None,
    surfaces: tuple[str, ...] = ("investigation",),
    injected_params: tuple[str, ...] | None = None,
    requires: list[str] | None = None,
    use_cases: list[str] | None = None,
    **kwargs: Any,
) -> Callable[[Any], Any]: ...


def plugin_tool[F: Callable[..., Any]](
    func: F | None = None,
    *,
    name: str,
    source: str,
    description: str,
    input_schema: dict[str, Any] | None = None,
    is_available: Callable[[dict[str, dict[str, Any]]], bool] | None = None,
    extract_params: Callable[[dict[str, dict[str, Any]]], dict[str, Any]] | None = None,
    surfaces: tuple[str, ...] = ("investigation",),
    injected_params: tuple[str, ...] | None = None,
    requires: list[str] | None = None,
    use_cases: list[str] | None = None,
    **kwargs: Any,
) -> Any:
    """Validate *input_schema* then delegate to OpenSRE's ``@tool`` decorator."""
    validate_tool_schema(input_schema, tool_name=name)

    opensre_tool = _opensre_tool()
    if opensre_tool is None:

        def offline_wrapper(inner: F) -> F:
            return _attach_offline_stub(inner, name=name, source=source, input_schema=input_schema)

        if func is None:
            return offline_wrapper
        return offline_wrapper(func)

    decorator = opensre_tool(
        name=name,
        source=source,
        description=description,
        input_schema=input_schema,
        is_available=is_available,
        extract_params=extract_params,
        surfaces=surfaces,
        injected_params=injected_params,
        requires=requires,
        use_cases=use_cases,
        **kwargs,
    )

    if func is None:
        return decorator
    return cast(F, decorator(func))
