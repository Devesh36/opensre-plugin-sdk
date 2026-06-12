# Contributing to opensre-plugin-sdk

Thanks for helping build the external plugin path for [OpenSRE](https://github.com/Tracer-Cloud/opensre).

## Development setup

```bash
git clone https://github.com/Devesh36/opensre-plugin-sdk.git
cd opensre-plugin-sdk
uv sync --extra dev
uv pip install -e ../opensre   # optional, for integration tests
```

## Quality bar (match OpenSRE)

Before opening a PR, all of the following must pass:

```bash
uv run ruff check src/ tests/ examples/ scripts/
uv run ruff format --check src/ tests/ examples/ scripts/
uv run mypy src/
uv run pytest tests/ -m "not integration" -v
uv run pytest tests/ -m integration -v   # requires opensre installed
```

## What to contribute

- **Schema contract fixes** when OpenSRE investigation tool rules change upstream
- **CLI improvements** (`init`, `validate`, `register`)
- **Reference plugins** under `examples/` (prefer mock/offline tools for CI)
- **Docs** — README, `docs/DEMO.md`, upstream PR templates

## Plugin authoring

1. `opensre-plugin init mytool`
2. Implement `client.py` and `tools/*.py` (one tool per file under `tools/`)
3. `opensre-plugin validate .`
4. Add `[tool.opensre-plugin]` to `pyproject.toml`
5. Test with `register_tools()` before shipping

See [investigation tool calling](https://github.com/Tracer-Cloud/opensre/blob/main/docs/investigation-tool-calling.md) for schema rules.

## Pull request checklist

- [ ] `ruff check` and `ruff format --check` pass
- [ ] `mypy src/` passes
- [ ] Unit tests pass without `opensre` installed
- [ ] Integration tests pass with `opensre` installed (if touching loader/registry)
- [ ] `opensre-plugin validate` passes on affected example plugins
- [ ] CHANGELOG.md updated for user-visible changes

## Code style

- Python 3.12+
- `from __future__ import annotations` in every module
- 100-character line length (ruff)
- Strict mypy on `src/opensre_plugin/`

## Reporting issues

Open a [GitHub issue](https://github.com/Devesh36/opensre-plugin-sdk/issues) with:

- SDK version or git commit
- `opensre-plugin validate` output (if applicable)
- Minimal plugin reproducer when reporting registration/schema bugs

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.
