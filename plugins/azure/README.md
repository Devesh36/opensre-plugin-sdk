# opensre-plugin-azure

Bridged OpenSRE **azure** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AZURE_LOG_ANALYTICS_WORKSPACE_ID`

## Tools

- `query_azure_monitor_logs`

## Install

```bash
pip install -e plugins/azure
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/azure
```
