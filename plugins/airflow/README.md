# opensre-plugin-airflow

Bridged OpenSRE **airflow** integration (3 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AIRFLOW_BASE_URL`

## Tools

- `get_airflow_dag_runs`
- `get_airflow_task_instances`
- `get_recent_airflow_failures`

## Install

```bash
pip install -e plugins/airflow
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/airflow
```
