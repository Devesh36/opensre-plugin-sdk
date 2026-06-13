"""ec2 plugin — bridged from OpenSRE core tools."""

from __future__ import annotations


def register() -> None:
    from ec2_plugin import tools
    from opensre_plugin.loader import register_tools

    register_tools(tools)
