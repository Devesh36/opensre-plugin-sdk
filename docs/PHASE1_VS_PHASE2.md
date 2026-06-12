# Phase 1 vs Phase 2

Honest scope boundaries for external plugins today vs what requires OpenSRE core team buy-in.

## Phase 1 — works today (no core changes)

| Capability | How |
|------------|-----|
| Ship external tool packages | `register_tools()` → `register_external_tool_package()` |
| Strict schema validation | `opensre-plugin validate`, `@plugin_tool` |
| CLI scaffolding | `opensre-plugin init` |
| Env-based credentials | `is_available` + `extract_params` reading `os.environ` |
| Hide secrets from LLM | `injected_params` |
| Multiple plugins | Separate packages or monorepo; each calls `register()` |
| Investigation loop | Tools appear in `get_registered_tools("investigation")` after registration |

### What you ship in a Phase 1 plugin

```toml
[tool.opensre-plugin]
name = "linear"
tools_package = "linear_plugin.tools"
```

```python
@plugin_tool(..., is_available=..., extract_params=..., injected_params=...)
def my_tool(query: str, api_key: str) -> dict: ...
```

```bash
export VENDOR_API_KEY=...
python -c "from my_plugin import register; register()"
opensre investigate --alert '...'
```

### Phase 1 limitations

- **Manual registration** — plugins are not auto-loaded at `opensre` startup
- **No catalog entry** — plugin won't appear in `opensre integrations list`
- **No onboard wizard** — no `opensre onboard` step for your vendor
- **No verify probe** — `opensre integrations verify` won't test your API
- **Closed `EvidenceSource`** — reuse an existing literal (e.g. `"github"`) or propose Phase 2
- **No multi-instance store** — env vars, not encrypted integration store

## Phase 2 — needs core changes

| Capability | Core touchpoints |
|------------|------------------|
| Entry-point auto-discovery | `app/tools/registry.py`, `[project.entry-points."opensre.plugins"]` RFC |
| Integration catalog | `_catalog_impl.py`, `IntegrationSpec.classifier` |
| Onboard wizard step | `opensre onboard` flows |
| Verify probes | `opensre integrations verify`, `_verification_adapters.py` |
| New evidence sources | `app/types/evidence.py`, docs |
| Plugin index | `opensre integrations list --plugins` (proposal) |
| Synthetic fixtures | `tests/synthetic/` export from plugins |

### Proposed upstream work (not in this SDK repo)

1. **Docs-only PR** — link to SDK from OpenSRE docs ([`docs/upstream-pr/`](upstream-pr/) ready, open after maintainer feedback)
2. **Entry-point RFC** — auto-load plugins on `opensre` import
3. **`PluginIntegrationSpec`** — hooks for catalog classifier / env_loader from manifest

## Decision guide

| Goal | Phase |
|------|-------|
| Add a search tool for investigations | **Phase 1** |
| Gate on env var API key | **Phase 1** |
| Appear in integration catalog UI | Phase 2 |
| `opensre integrations verify myvendor` | Phase 2 |
| Zero manual `register()` call | Phase 2 |

## SDK commitment

Phase 1 features are stable in `opensre-plugin-sdk` v0.1.x. Schema contract tracks OpenSRE's strictest investigation adapter; pin versions if you depend on specific OpenSRE releases.

Phase 2 items will be proposed to Tracer-Cloud/opensre as small, reviewable PRs — not bundled into the SDK as workarounds.

## Related

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [AUTHORING.md](AUTHORING.md)
- [FAQ.md](FAQ.md)
