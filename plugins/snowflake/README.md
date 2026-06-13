# opensre-plugin-snowflake

Bridged OpenSRE **snowflake** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `SNOWFLAKE_TOKEN`
- `SNOWFLAKE_ACCOUNT`

## Tools

- `query_snowflake_history`

## Install

```bash
pip install -e plugins/snowflake
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/snowflake
```
