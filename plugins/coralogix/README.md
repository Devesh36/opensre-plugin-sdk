# opensre-plugin-coralogix

Bridged OpenSRE **coralogix** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `CORALOGIX_API_KEY`

## Tools

- `query_coralogix_logs`

## Install

```bash
pip install -e plugins/coralogix
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/coralogix
```
