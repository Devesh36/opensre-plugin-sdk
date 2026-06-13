# opensre-plugin-supabase

Bridged OpenSRE **supabase** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `SUPABASE_URL`

## Tools

- `get_supabase_service_health`
- `get_supabase_storage_buckets`

## Install

```bash
pip install -e plugins/supabase
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/supabase
```
