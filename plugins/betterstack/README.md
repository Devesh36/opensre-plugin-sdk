# opensre-plugin-betterstack

Bridged OpenSRE **betterstack** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `BETTERSTACK_QUERY_ENDPOINT`

## Tools

- `query_betterstack_logs`

## Install

```bash
pip install -e plugins/betterstack
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/betterstack
```
