# opensre-plugin-ec2

Bridged OpenSRE **ec2** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AWS_ACCESS_KEY_ID`
- `AWS_ROLE_ARN`

## Tools

- `ec2_instances_by_tag`
- `get_elb_target_health`

## Install

```bash
pip install -e plugins/ec2
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/ec2
```
