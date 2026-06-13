# opensre-plugin-twilio

Bridged OpenSRE **twilio** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `TWILIO_ACCOUNT_SID`

## Tools

- `twilio_notify`

## Install

```bash
pip install -e plugins/twilio
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/twilio
```
