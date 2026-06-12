"""``@plugin_tool`` decorator — validated wrapper over OpenSRE's ``@tool``."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast, overload

from opensre_plugin.exceptions import OpensreNotInstalledError
from opensre_plugin.schema.validator import validate_tool_schema


def _opensre_tool() -> Any:
    try:
        from app.tools.tool_decorator import tool
    except ImportError as exc:
        raise OpensreNotInstalledError("the @plugin_tool decorator") from exc
    return tool


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

    tool = _opensre_tool()
    decorator = tool(
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
