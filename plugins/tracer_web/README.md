# opensre-plugin-tracer-web

Bridged OpenSRE **tracer_web** integration (7 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `JWT_TOKEN`
- `TRACER_API_URL`

## Tools

- `fetch_failed_run`
- `get_airflow_metrics`
- `get_batch_statistics`
- `get_error_logs`
- `get_failed_tools`
- `get_tracer_run`
- `get_tracer_tasks`

## Install

```bash
pip install -e plugins/tracer_web
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/tracer_web
```
