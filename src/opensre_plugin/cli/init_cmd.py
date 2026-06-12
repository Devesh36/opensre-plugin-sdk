"""``opensre-plugin init`` command."""

from __future__ import annotations

import re
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader, StrictUndefined


def _normalize_name(raw: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", raw.strip().lower()).strip("_")
    if not slug:
        raise click.ClickException("Plugin name must contain at least one letter or digit.")
    if slug[0].isdigit():
        slug = f"plugin_{slug}"
    return slug


def _render_templates(name: str, output: Path) -> None:
    slug = _normalize_name(name)
    plugin_name = f"{slug}_plugin"
    tool_name = slug.replace("-", "_")
    package_name = plugin_name.replace("-", "_")
    class_prefix = "".join(part.capitalize() for part in re.split(r"[_-]+", slug))

    template_dir = Path(__file__).resolve().parents[3] / "templates" / "tool_plugin"
    if not template_dir.is_dir():
        raise click.ClickException(f"Template directory not found: {template_dir}")

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    context = {
        "name": slug,
        "plugin_name": plugin_name,
        "tool_name": tool_name,
        "package_name": package_name,
        "class_prefix": class_prefix,
    }

    for template_path in sorted(template_dir.rglob("*.j2")):
        rel = str(template_path.relative_to(template_dir)).replace("\\", "/")
        rendered_rel = env.from_string(rel).render(**context)
        if rendered_rel.endswith(".j2"):
            rendered_rel = rendered_rel[:-3]
        out_path = output / rendered_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        template = env.get_template(rel)
        out_path.write_text(template.render(**context), encoding="utf-8")


@click.command("init")
@click.argument("name")
@click.option(
    "--output",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Directory to create the plugin in (default: cwd).",
)
def init(name: str, output: Path | None) -> None:
    """Scaffold a new OpenSRE tool plugin."""
    slug = _normalize_name(name)
    plugin_name = f"{slug}_plugin"
    target = (output or Path.cwd()) / plugin_name

    if target.exists():
        raise click.ClickException(f"Directory already exists: {target}")

    _render_templates(name, target)

    click.echo(f"Created plugin scaffold at {target}/")
    click.echo("")
    click.echo("Next steps:")
    click.echo(f"  1. cd {plugin_name}")
    click.echo("  2. Implement client.py and tools/")
    click.echo("  3. opensre-plugin validate .")
    click.echo(f"  4. export {slug.upper()}_API_KEY=...")
    click.echo(f'  5. python -c "from {plugin_name} import register; register()"')
    click.echo("  6. opensre investigate --alert '...'")
