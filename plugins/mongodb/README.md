# opensre-plugin-mongodb

Bridged OpenSRE **mongodb** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `MONGODB_CONNECTION_STRING`

## Tools

- `get_mongodb_collection_stats`
- `get_mongodb_current_ops`
- `get_mongodb_profiler_data`
- `get_mongodb_replica_status`
- `get_mongodb_server_status`

## Install

```bash
pip install -e plugins/mongodb
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/mongodb
```
