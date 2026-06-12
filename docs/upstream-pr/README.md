# Upstream docs PR for OpenSRE

**Status: ready, not opened.** Use this folder only after an OpenSRE maintainer says the SDK looks good.

Copy these files into [Tracer-Cloud/opensre](https://github.com/Tracer-Cloud/opensre) as a **docs-only PR** linking to the external plugin SDK.

## Files to add

| This repo | OpenSRE destination |
|-----------|---------------------|
| `plugin-sdk.mdx` | `docs/plugin-sdk.mdx` |
| `docs.json.snippet` | merge into `docs/docs.json` under `"navigation"` |
| `contributing.snippet.md` | append link in `CONTRIBUTING.md` (line ~18) |

## Suggested PR title

```
docs: link external plugin SDK for third-party investigation tools
```

## Suggested PR body

```markdown
## Summary

- Adds `docs/plugin-sdk.mdx` — community guide for external tool plugins
- Links to the standalone `opensre-plugin-sdk` repo (schema validation, CLI, reference plugin)
- Completes the plugin path referenced in CONTRIBUTING.md

## Test plan

- [ ] Mintlify preview renders `plugin-sdk.mdx`
- [ ] Navigation entry appears in docs sidebar
- [ ] No runtime/code changes — docs only
```

## Discord #contribute post (after SDK repo is public)

```text
Built an external plugin SDK for OpenSRE — completes the plugin path documented
in CONTRIBUTING.md ("third-party plugins via the plugin SDK") that isn't
implemented yet.

- SDK: https://github.com/YOU/opensre-plugin-sdk
  - Schema validator (ports investigation_tool_schema_contract)
  - Loader around register_external_tool_package()
  - CLI: opensre-plugin init / validate

- Demo plugin: examples/linear in the SDK repo
  - External tool package, no _catalog_impl.py changes
  - Validated against opensre @ v0.1

Happy to open a docs-only PR linking to this, or walk through a 5-min demo.
```

Replace `YOU` with your GitHub org/username before posting.
