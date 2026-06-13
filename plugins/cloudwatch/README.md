# opensre-plugin-cloudwatch

Bridged OpenSRE **cloudwatch** integration (8 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AWS_ACCESS_KEY_ID`
- `AWS_ROLE_ARN`

## Tools

- `get_cloudwatch_batch_metrics`
- `get_cloudwatch_logs`
- `get_host_metrics`
- `get_lambda_configuration`
- `get_lambda_errors`
- `get_lambda_invocation_logs`
- `get_lambda_invocation_logs`
- `inspect_lambda_function`

## Install

```bash
pip install -e plugins/cloudwatch
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/cloudwatch
```
