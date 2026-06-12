"""Mock plugin entry point."""

from __future__ import annotations


def register() -> None:
    """Register mock tools with OpenSRE."""
    from mock_plugin import tools
    from opensre_plugin.loader import register_tools

    register_tools(tools)
