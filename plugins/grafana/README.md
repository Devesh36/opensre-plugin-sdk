# opensre-plugin-grafana

Bridged OpenSRE **grafana** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `GRAFANA_INSTANCE_URL`

## Tools

- `query_grafana_alert_rules`
- `query_grafana_logs`
- `query_grafana_metrics`
- `query_grafana_service_names`
- `query_grafana_traces`

## Install

```bash
pip install -e plugins/grafana
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/grafana
```
