# opensre-plugin-splunk

Bridged OpenSRE **splunk** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `SPLUNK_URL`

## Tools

- `query_splunk_logs`

## Install

```bash
pip install -e plugins/splunk
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/splunk
```
