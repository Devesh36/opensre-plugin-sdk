# opensre-plugin-helm

Bridged OpenSRE **helm** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `OSRE_HELM_INTEGRATION`

## Tools

- `helm_get_release_manifest`
- `helm_get_release_values`
- `helm_list_releases`
- `helm_release_history`
- `helm_release_status`

## Install

```bash
pip install -e plugins/helm
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/helm
```
