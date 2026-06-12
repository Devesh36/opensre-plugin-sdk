# Authoring plugins

How to write `is_available`, `extract_params`, and `injected_params` — the CloudOpsBench / Linear pattern for Phase 1 plugins.

## Tool anatomy

```python
@plugin_tool(
    name="search_linear_issues",
    source="github",                    # existing EvidenceSource literal
    description="...",
    input_schema={...},                 # LLM-visible params only
    is_available=_linear_available,
    extract_params=_linear_extract_params,
    injected_params=("api_key",),       # hidden from LLM
    requires=["api_key"],               # documentation / metadata
)
def search_linear_issues(query: str, api_key: str) -> dict[str, Any]:
    ...
```

## Return contract

`run()` must **never** raise unhandled exceptions to the investigation loop.

| Outcome | Shape |
|---------|-------|
| Success | `{"success": True, ...}` |
| Failure | `{"error": "human-readable message"}` |

## `is_available(sources) -> bool`

Called before the tool is included in the LLM tool list.

```python
def _linear_available(sources: dict[str, dict]) -> bool:
    _ = sources  # Phase 1: env-based, ignore sources
    return bool(os.environ.get("LINEAR_API_KEY"))
```

**Purpose:** Hide the tool when credentials are missing so the LLM doesn't call a tool that will fail.

### CloudOpsBench pattern — gate on `sources` slot

Production plugins can read resolved integration state from `sources`:

```python
def _cloudops_available(sources: dict[str, dict]) -> bool:
    return (sources.get("eks") or {}).get("_bench_backend") is not None
```

Phase 1 external plugins typically gate on **env vars** because they don't wire into `_catalog_impl.py` yet.

## `extract_params(sources) -> dict`

Maps integration context → kwargs passed to `run()` alongside LLM-provided args.

```python
def _linear_extract_params(sources: dict[str, dict]) -> dict[str, Any]:
    _ = sources
    return {"api_key": os.environ.get("LINEAR_API_KEY", "")}
```

Investigation merges: `{**extract_params(sources), **llm_tool_call_input}`.

### CloudOpsBench — inject backend + defaults

```python
def _extract_get_resources(sources: dict[str, dict]) -> dict[str, Any]:
    backend = _cloudops_backend(sources)
    return {
        "cloudops_backend": backend,
        "resource_type": _resource_type_from_process(backend),
        "namespace": _default_namespace(backend, sources),
    }
```

## `injected_params` — hide secrets and backends from the LLM

**Critical:** Without `injected_params`, the LLM sees `api_key` or `cloudops_backend` in the schema and may pass garbage strings. Dispatch merges LLM input over injected params, so a string from the LLM can **override** the real backend object.

CloudOpsBench documents this explicitly:

```text
injected_params=("cloudops_backend",)
→ backend hidden from LLM schema
→ supplied by extract_params at call time
```

### Rules

1. List every param in `injected_params` that the LLM must **not** control (API keys, clients, backends).
2. Do **not** put injected param names in `input_schema.properties`.
3. Include them as function parameters: `def run(query: str, api_key: str)`.
4. Return them from `extract_params`.

### Linear example (env key)

```python
injected_params=("api_key",),

def _linear_extract_params(sources: dict[str, dict]) -> dict[str, Any]:
    return {"api_key": get_api_key()}
```

LLM schema only shows `query`. `api_key` is injected server-side.

## Package layout

```
my_plugin/
├── pyproject.toml          # [tool.opensre-plugin]
├── my_plugin/
│   ├── __init__.py         # register()
│   ├── config.py           # env helpers
│   ├── client.py           # API client
│   └── tools/
│       ├── __init__.py     # empty package marker
│       └── search.py       # @plugin_tool here (not only in __init__.py)
```

OpenSRE walks `tools/` submodules. One tool per file is the safest pattern.

## Registration

```python
# my_plugin/__init__.py
def register() -> None:
    from opensre_plugin.loader import register_tools
    from my_plugin import tools
    register_tools(tools)
```

Call before `opensre investigate` in the **same Python process** (or use `opensre-plugin register .`).

## `source` field

`source` must be an existing OpenSRE `EvidenceSource` literal (e.g. `"github"`, `"eks"`, `"sentry"`). Phase 1 plugins reuse the closest match. Custom sources require Phase 2 core changes.

## Checklist

- [ ] `opensre-plugin validate .` passes
- [ ] `input_schema` has no injected param names
- [ ] `injected_params` set for secrets/backends
- [ ] `is_available` returns `False` without credentials
- [ ] `run()` returns `{"error": "..."}` on failure, never raises
- [ ] Tools live in `tools/*.py` submodules
- [ ] `register()` called before investigation

## References

- [`examples/mock/`](../examples/mock/) — offline, `MOCK_API_KEY`
- [`examples/linear/`](../examples/linear/) — HTTP, `LINEAR_API_KEY`
- [CloudOpsBench k8s tools](https://github.com/Tracer-Cloud/opensre/blob/main/tests/benchmarks/cloudopsbench/tools/k8s/__init__.py)
