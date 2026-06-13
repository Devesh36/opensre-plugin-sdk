# opensre-plugin-victoria-logs

Bridged OpenSRE **victoria_logs** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `VICTORIA_LOGS_URL`

## Tools

- `victoria_logs_query`

## Install

```bash
pip install -e plugins/victoria_logs
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/victoria_logs
```
