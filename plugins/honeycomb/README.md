# opensre-plugin-honeycomb

Bridged OpenSRE **honeycomb** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `HONEYCOMB_API_KEY`

## Tools

- `query_honeycomb_traces`

## Install

```bash
pip install -e plugins/honeycomb
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/honeycomb
```
