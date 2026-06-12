"""Linear plugin entry point."""

from __future__ import annotations


def register() -> None:
    from opensre_plugin.loader import register_tools

    from linear_plugin import tools

    register_tools(tools)
