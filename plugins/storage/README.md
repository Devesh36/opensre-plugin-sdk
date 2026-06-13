# opensre-plugin-storage

Bridged OpenSRE **storage** integration (4 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AWS_ACCESS_KEY_ID`
- `AWS_ROLE_ARN`

## Tools

- `check_s3_marker`
- `get_s3_object`
- `inspect_s3_object`
- `list_s3_objects`

## Install

```bash
pip install -e plugins/storage
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/storage
```
