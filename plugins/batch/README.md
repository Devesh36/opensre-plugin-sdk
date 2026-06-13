# opensre-plugin-batch

Bridged OpenSRE **batch** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `JWT_TOKEN`
- `TRACER_API_URL`

## Tools

- `get_failed_jobs`

## Install

```bash
pip install -e plugins/batch
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/batch
```
