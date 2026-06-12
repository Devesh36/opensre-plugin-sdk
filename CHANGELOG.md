# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-06-12

### Added

- **Schema validator** — ports OpenSRE `investigation_tool_schema_contract` invariants; works without `opensre` installed
- **`SchemaValidationError`** with `tool_name`, JSON path, and message
- **`@plugin_tool` decorator** — validates `input_schema` at decoration time, delegates to OpenSRE `@tool`
- **Plugin loader** — `register_tools()`, `register_from_manifest()`, `clear_and_register()`, `list_plugin_tools()`
- **Manifest parser** — `[tool.opensre-plugin]` table from `pyproject.toml`
- **CLI** — `opensre-plugin init`, `validate`, `register`
- **Templates** — `templates/tool_plugin/` for `opensre-plugin init`
- **Reference plugins**
  - `examples/linear` — Linear GraphQL issue search (`LINEAR_API_KEY`)
  - `examples/mock` — offline in-memory search (`MOCK_API_KEY`, no network)
- **Tests** — 35+ unit and integration tests
- **CI** — ruff, mypy, pytest on push/PR
- **Publish workflow** — PyPI on GitHub release (requires `PYPI_API_TOKEN`)
- **Docs** — README, `docs/DEMO.md`, upstream PR template in `docs/upstream-pr/`
- **`scripts/demo_e2e.py`** — smoke test for validate → register → tool run

### Notes

- Phase 1 scope: external tool packages only; no OpenSRE core catalog changes
- Tools must live in package **submodules** under `tools/` (e.g. `tools/search.py`), not only in `tools/__init__.py`

[0.1.0]: https://github.com/Devesh36/opensre-plugin-sdk/releases/tag/v0.1.0
