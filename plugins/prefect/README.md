# opensre-plugin-prefect

Bridged OpenSRE **prefect** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `PREFECT_API_KEY`

## Tools

- `prefect_flow_runs`
- `prefect_worker_health`

## Install

```bash
pip install -e plugins/prefect
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/prefect
```
