# opensre-plugin-sentry

Bridged OpenSRE **sentry** integration (3 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `SENTRY_AUTH_TOKEN`

## Tools

- `get_sentry_issue_details`
- `list_sentry_issue_events`
- `search_sentry_issues`

## Install

```bash
pip install -e plugins/sentry
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/sentry
```
