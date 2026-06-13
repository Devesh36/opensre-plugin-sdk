# opensre-plugin-openclaw

Bridged OpenSRE **openclaw** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `OPENCLAW_MCP_URL`
- `OPENCLAW_MCP_COMMAND`

## Tools

- `call_openclaw_tool`
- `get_openclaw_conversation`
- `list_openclaw_tools`
- `search_openclaw_conversations`
- `send_openclaw_message`

## Install

```bash
pip install -e plugins/openclaw
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/openclaw
```
