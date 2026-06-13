# opensre-plugin-bitbucket

Bridged OpenSRE **bitbucket** integration (3 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `BITBUCKET_APP_PASSWORD`
- `BITBUCKET_USERNAME`

## Tools

- `get_bitbucket_file_contents`
- `list_bitbucket_commits`
- `search_bitbucket_code`

## Install

```bash
pip install -e plugins/bitbucket
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/bitbucket
```
