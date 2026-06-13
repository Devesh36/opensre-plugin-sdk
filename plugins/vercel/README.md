# opensre-plugin-vercel

Bridged OpenSRE **vercel** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `VERCEL_API_TOKEN`

## Tools

- `vercel_deployment_logs`
- `vercel_deployment_status`

## Install

```bash
pip install -e plugins/vercel
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/vercel
```
