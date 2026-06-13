# opensre-plugin-azure-sql

Bridged OpenSRE **azure_sql** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AZURE_SQL_SERVER`

## Tools

- `get_azure_sql_current_queries`
- `get_azure_sql_resource_stats`
- `get_azure_sql_server_status`
- `get_azure_sql_slow_queries`
- `get_azure_sql_wait_stats`

## Install

```bash
pip install -e plugins/azure_sql
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/azure_sql
```
