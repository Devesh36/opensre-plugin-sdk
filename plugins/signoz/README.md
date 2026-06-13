# opensre-plugin-signoz

Bridged OpenSRE **signoz** integration (3 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `SIGNOZ_URL`

## Tools

- `query_signoz_logs`
- `query_signoz_metrics`
- `query_signoz_traces`

## Install

```bash
pip install -e plugins/signoz
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/signoz
```
