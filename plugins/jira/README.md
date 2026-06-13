# opensre-plugin-jira

Bridged OpenSRE **jira** integration (4 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `JIRA_API_TOKEN`

## Tools

- `jira_add_comment`
- `jira_create_issue`
- `jira_issue_detail`
- `jira_search_issues`

## Install

```bash
pip install -e plugins/jira
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/jira
```
