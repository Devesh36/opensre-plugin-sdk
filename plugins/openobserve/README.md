# opensre-plugin-openobserve

Bridged OpenSRE **openobserve** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `OPENOBSERVE_URL`

## Tools

- `query_openobserve_logs`

## Install

```bash
pip install -e plugins/openobserve
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/openobserve
```
