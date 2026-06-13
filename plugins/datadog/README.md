# opensre-plugin-datadog

Bridged OpenSRE **datadog** integration (6 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `DD_API_KEY`

## Tools

- `get_pods_on_node`
- `query_datadog_all`
- `query_datadog_events`
- `query_datadog_logs`
- `query_datadog_metrics`
- `query_datadog_monitors`

## Install

```bash
pip install -e plugins/datadog
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/datadog
```
