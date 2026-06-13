# opensre-plugin-postgresql

Bridged OpenSRE **postgresql** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `POSTGRESQL_HOST`

## Tools

- `get_postgresql_current_queries`
- `get_postgresql_replication_status`
- `get_postgresql_server_status`
- `get_postgresql_slow_queries`
- `get_postgresql_table_stats`

## Install

```bash
pip install -e plugins/postgresql
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/postgresql
```
