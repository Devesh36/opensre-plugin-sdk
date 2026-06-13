# opensre-plugin-rds

Bridged OpenSRE **rds** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AWS_ACCESS_KEY_ID`
- `AWS_ROLE_ARN`
- `RDS_DB_INSTANCE_IDENTIFIER`

## Tools

- `describe_rds_events`
- `describe_rds_instance`

## Install

```bash
pip install -e plugins/rds
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/rds
```
