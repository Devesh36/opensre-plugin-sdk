# opensre-plugin-opensearch

Bridged OpenSRE **opensearch** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `OPENSEARCH_URL`

## Tools

- `query_opensearch_analytics`

## Install

```bash
pip install -e plugins/opensearch
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/opensearch
```
