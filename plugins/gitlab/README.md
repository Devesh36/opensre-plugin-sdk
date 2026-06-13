# opensre-plugin-gitlab

Bridged OpenSRE **gitlab** integration (4 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `GITLAB_ACCESS_TOKEN`

## Tools

- `get_gitlab_file`
- `list_gitlab_commits`
- `list_gitlab_mrs`
- `list_gitlab_pipelines`

## Install

```bash
pip install -e plugins/gitlab
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/gitlab
```
