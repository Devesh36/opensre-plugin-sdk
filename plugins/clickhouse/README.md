# opensre-plugin-clickhouse

Bridged OpenSRE **clickhouse** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `CLICKHOUSE_HOST`

## Tools

- `get_clickhouse_query_activity`
- `get_clickhouse_system_health`

## Install

```bash
pip install -e plugins/clickhouse
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/clickhouse
```
