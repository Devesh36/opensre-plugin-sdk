# opensre-plugin-github

Bridged OpenSRE **github** integration (9 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `GITHUB_MCP_URL`
- `GITHUB_MCP_COMMAND`

## Tools

- `get_git_deploy_timeline`
- `get_github_actions_step_log`
- `get_github_file_contents`
- `get_github_repository_tree`
- `list_github_actions_active_runs`
- `list_github_actions_run_jobs`
- `list_github_actions_workflow_runs`
- `list_github_commits`
- `search_github_code`

## Install

```bash
pip install -e plugins/github
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/github
```
