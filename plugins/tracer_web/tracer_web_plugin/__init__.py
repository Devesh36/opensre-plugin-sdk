"""tracer_web plugin — bridged from OpenSRE core tools."""

from __future__ import annotations


def register() -> None:
    from tracer_web_plugin import tools
    from opensre_plugin.loader import register_tools

    register_tools(tools)
