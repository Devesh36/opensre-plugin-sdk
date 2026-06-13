# opensre-plugin-aws-sdk

Bridged OpenSRE **aws_sdk** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AWS_ACCESS_KEY_ID`
- `AWS_ROLE_ARN`

## Tools

- `execute_aws_operation`

## Install

```bash
pip install -e plugins/aws_sdk
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/aws_sdk
```
