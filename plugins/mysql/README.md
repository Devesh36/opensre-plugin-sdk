# opensre-plugin-mysql

Bridged OpenSRE **mysql** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `MYSQL_HOST`

## Tools

- `get_mysql_current_processes`
- `get_mysql_replication_status`
- `get_mysql_server_status`
- `get_mysql_slow_queries`
- `get_mysql_table_stats`

## Install

```bash
pip install -e plugins/mysql
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/mysql
```
