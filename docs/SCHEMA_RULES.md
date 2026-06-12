# Schema rules

Investigation sends **every available** tool schema in a **single** LLM invoke. One invalid schema fails the entire request (HTTP 400, "invalid tools", etc.) — even when the alert never uses that tool.

The SDK ports invariants from OpenSRE's [`investigation_tool_schema_contract.py`](https://github.com/Tracer-Cloud/opensre/blob/main/tests/services/investigation_tool_schema_contract.py) and [`investigation-tool-calling.md`](https://github.com/Tracer-Cloud/opensre/blob/main/docs/investigation-tool-calling.md).

Validate before every release:

```bash
opensre-plugin validate .
```

## Top-level shape

Every investigation tool `input_schema` must be:

```json
{
  "type": "object",
  "properties": { ... },
  "required": ["..."]
}
```

## Rules

| Rule | Why | Valid | Invalid |
|------|-----|-------|---------|
| Single string `type` | Strict LLM APIs reject union types | `"type": "string"` | `"type": ["string", "null"]` |
| Typed array `items` | Bare arrays fail adapter | `"items": {"type": "string"}` | `"type": "array"` with no `items` |
| Non-empty `items` | Empty `{}` items fail | `"items": {"type": "object", "properties": {...}}` | `"items": {}` |
| No `$ref` / `$defs` | Adapters don't resolve refs | inline `properties` | `"$ref": "#/definitions/Foo"` |
| No `nullable` | Use optional fields instead | omit from `required` | `"nullable": true` |
| No `title` / `$schema` | Stripped by strict normalizers | — | `"title": "MyTool"` |

### Unsupported keys (rejected by SDK)

`title`, `$schema`, `$defs`, `definitions`, `$ref`, `not`, `nullable`

## Examples

### Valid — minimal search tool

```python
input_schema={
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Search query",
        },
    },
    "required": ["query"],
}
```

### Valid — nested object and array

```python
input_schema={
    "type": "object",
    "properties": {
        "filter": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "severity": {"type": "string"},
            },
            "required": ["service"],
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["filter"],
}
```

### Invalid — type union (common mistake)

```python
# FAILS: type must not be a list ['object', 'null']
"properties": {
    "credentials": {
        "type": ["object", "null"],
        "properties": {"token": {"type": "string"}},
    }
}
```

Error:

```text
tool 'my_tool' at 'properties.credentials.type': type must not be a list ['object', 'null']
```

### Invalid — array without items

```python
# FAILS: array missing typed items
"properties": {
    "ids": {"type": "array"}
}
```

### Invalid — `$ref`

```python
# FAILS: unsupported key '$ref'
"properties": {
    "payload": {"$ref": "#/definitions/Foo"}
}
```

## Injected parameters

Parameters listed in `injected_params` (e.g. `api_key`, `cloudops_backend`) are **removed** from the schema the LLM sees. They should **not** appear in `input_schema.properties`.

The LLM only sees public parameters; `extract_params` supplies injected values at dispatch time.

## Optional fields

Do **not** use `"type": ["string", "null"]`. Instead:

- Omit the field from `required`
- Use a single string type: `"type": "string"`
- Let the LLM omit optional keys

## When rules change upstream

If OpenSRE adds a stricter adapter, pin SDK releases and update `schema/validator.py` + contract tests in the same PR. The SDK semver should track schema contract changes.

## Related

- [AUTHORING.md](AUTHORING.md) — `input_schema` + `injected_params` together
- [ARCHITECTURE.md](ARCHITECTURE.md) — where validation runs in the pipeline
