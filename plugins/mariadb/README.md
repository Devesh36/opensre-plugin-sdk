# opensre-plugin-mariadb

Bridged OpenSRE **mariadb** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `MARIADB_HOST`

## Tools

- `get_mariadb_global_status`
- `get_mariadb_innodb_status`
- `get_mariadb_process_list`
- `get_mariadb_replication_status`
- `get_mariadb_slow_queries`

## Install

```bash
pip install -e plugins/mariadb
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/mariadb
```
