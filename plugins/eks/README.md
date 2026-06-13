# opensre-plugin-eks

Bridged OpenSRE **eks** integration (11 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `AWS_ACCESS_KEY_ID`
- `AWS_ROLE_ARN`

## Tools

- `describe_eks_addon`
- `describe_eks_cluster`
- `get_eks_deployment_status`
- `get_eks_events`
- `get_eks_node_health`
- `get_eks_nodegroup_health`
- `get_eks_pod_logs`
- `list_eks_clusters`
- `list_eks_deployments`
- `list_eks_namespaces`
- `list_eks_pods`

## Install

```bash
pip install -e plugins/eks
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/eks
```
