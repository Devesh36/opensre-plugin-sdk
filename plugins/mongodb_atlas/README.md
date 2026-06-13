# opensre-plugin-mongodb-atlas

Bridged OpenSRE **mongodb_atlas** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `MONGODB_ATLAS_PUBLIC_KEY`

## Tools

- `get_mongodb_atlas_alerts`
- `get_mongodb_atlas_cluster_events`
- `get_mongodb_atlas_cluster_metrics`
- `get_mongodb_atlas_clusters`
- `get_mongodb_atlas_performance_advisor`

## Install

```bash
pip install -e plugins/mongodb_atlas
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/mongodb_atlas
```
