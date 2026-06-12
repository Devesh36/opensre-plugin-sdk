"""OpenSRE plugin SDK CLI."""

from __future__ import annotations

import click

from opensre_plugin.cli.init_cmd import init
from opensre_plugin.cli.validate_cmd import register, validate


@click.group()
def main() -> None:
    """OpenSRE plugin SDK — scaffold and validate external investigation tools."""


main.add_command(init)
main.add_command(validate)
main.add_command(register)
