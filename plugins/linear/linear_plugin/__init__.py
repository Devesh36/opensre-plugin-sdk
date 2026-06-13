"""Linear plugin entry point."""

from __future__ import annotations


def register() -> None:
    from linear_plugin import tools
    from opensre_plugin.loader import register_tools

    register_tools(tools)
