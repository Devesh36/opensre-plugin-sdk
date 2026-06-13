# opensre-plugin-knowledge

Bridged OpenSRE **knowledge** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- No credentials required

## Tools

- `get_sre_guidance`
- `run_diagnostic_code`

## Install

```bash
pip install -e plugins/knowledge
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/knowledge
```
