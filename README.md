# opensre-plugin-sdk

[![ci](https://github.com/Devesh36/opensre-plugin-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/Devesh36/opensre-plugin-sdk/actions/workflows/ci.yml)

SDK for building external [OpenSRE](https://github.com/Tracer-Cloud/opensre) investigation tool plugins without modifying the core repository.

OpenSRE's `CONTRIBUTING.md` states that *"Most feature ideas are better shipped as third-party plugins via the plugin SDK"* — this package implements that path.

## Install

**From GitHub** (recommended until PyPI is published):

```bash
pip install "opensre-plugin-sdk @ git+https://github.com/Devesh36/opensre-plugin-sdk.git@v0.1.0"
```

Editable local install for development:

```bash
git clone https://github.com/Devesh36/opensre-plugin-sdk.git
cd opensre-plugin-sdk
pip install -e ".[dev]"
```

**From PyPI** (after `v0.1.0` is published):

```bash
pip install opensre-plugin-sdk
```

With OpenSRE integration helpers:

```bash
pip install "opensre-plugin-sdk[opensre] @ git+https://github.com/Devesh36/opensre-plugin-sdk.git@v0.1.0"
pip install opensre
```

## Quick start

```bash
pip install "opensre-plugin-sdk @ git+https://github.com/Devesh36/opensre-plugin-sdk.git@v0.1.0"

# Scaffold a new plugin
opensre-plugin init linear
cd linear_plugin

# Validate schemas offline (no opensre required)
opensre-plugin validate .

# Register with OpenSRE
pip install opensre
pip install -e .
export LINEAR_API_KEY=lin_api_xxx
python -c "from linear_plugin import register; register()"

# Run an investigation
opensre investigate --alert '{"title": "Payment API 500 errors"}'
```

See [`examples/linear/`](examples/linear/) for a real API integration and [`examples/mock/`](examples/mock/) for an offline demo with no network. Proof transcript: [`docs/DEMO.md`](docs/DEMO.md).

## Architecture

```text
Your plugin (@plugin_tool tools)
        ↓
opensre-plugin-sdk (schema validation + loader)
        ↓
opensre.app.tools.registry.register_external_tool_package()
        ↓
get_registered_tools("investigation") → investigation ReAct loop
```

## Schema rules

Investigation sends **all** tool schemas in one LLM request. Invalid schemas break every investigation. The SDK enforces strict rules at the plugin boundary:

- Top-level `type: object` with `properties`
- Single string `type` per node (no `["object", "null"]` unions)
- Arrays must have typed `items`
- Unsupported keys rejected: `title`, `$schema`, `$ref`, `$defs`, `nullable`, etc.

Run `opensre-plugin validate` before shipping.

## Plugin manifest

Add to your plugin's `pyproject.toml`:

```toml
[tool.opensre-plugin]
name = "linear"
tools_package = "linear_plugin.tools"
description = "Linear issue search tools for OpenSRE investigations"
```

## CLI

| Command | Description |
|---------|-------------|
| `opensre-plugin init <name>` | Scaffold a new tool plugin |
| `opensre-plugin validate [path]` | Offline manifest + schema validation |
| `opensre-plugin register [path]` | Register tools with OpenSRE (requires `opensre`) |

## Phase 1 vs Phase 2

**Phase 1 (today):** External tool packages, env-based credentials, `is_available` / `extract_params`, schema validation. No core repo changes.

**Phase 2 (future):** Integration catalog wiring, `opensre onboard`, verify probes, entry-point auto-discovery.

## Development

```bash
uv sync --extra dev
uv run pytest tests/ -m "not integration" -v
uv run ruff check src/ tests/
uv run mypy src/

# Integration tests (requires opensre)
uv pip install -e ../opensre
uv run pytest tests/ -m integration -v

# End-to-end smoke test (validate + register Linear plugin)
uv pip install -e ../opensre
uv run python scripts/demo_e2e.py
```

## Publishing

1. Create a [PyPI API token](https://pypi.org/manage/account/token/) and add `PYPI_API_TOKEN` to GitHub repo secrets.
2. Create a GitHub release (tag e.g. `v0.1.0`) — the `publish` workflow uploads to PyPI via `uv publish`.
3. Local dry run: `uv build && uv publish --dry-run`

## Upstream OpenSRE docs PR

See [`docs/upstream-pr/`](docs/upstream-pr/) for a docs-only PR template (`plugin-sdk.mdx`, `docs.json` snippet, CONTRIBUTING link).

## Related

- [OpenSRE](https://github.com/Tracer-Cloud/opensre)
- [Investigation tool calling guide](https://github.com/Tracer-Cloud/opensre/blob/main/docs/investigation-tool-calling.md)
- [CloudOpsBench external tools reference](https://github.com/Tracer-Cloud/opensre/blob/main/tests/benchmarks/cloudopsbench/tools/k8s/__init__.py)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md), and [SECURITY.md](SECURITY.md).

## License

Apache-2.0
