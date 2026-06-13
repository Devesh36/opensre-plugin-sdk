# opensre-plugin-argocd

Bridged OpenSRE **argocd** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `ARGOCD_BASE_URL`

## Tools

- `argocd_application_diff`
- `argocd_application_status`

## Install

```bash
pip install -e plugins/argocd
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/argocd
```
