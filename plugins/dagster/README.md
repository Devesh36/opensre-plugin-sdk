# opensre-plugin-dagster

Bridged OpenSRE **dagster** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `DAGSTER_ENDPOINT`

## Tools

- `get_dagster_run_logs`
- `list_dagster_assets`
- `list_dagster_runs`
- `list_dagster_schedule_ticks`
- `list_dagster_sensor_ticks`

## Install

```bash
pip install -e plugins/dagster
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/dagster
```
