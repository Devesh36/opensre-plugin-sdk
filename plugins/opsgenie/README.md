# opensre-plugin-opsgenie

Bridged OpenSRE **opsgenie** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `OPSGENIE_API_KEY`

## Tools

- `opsgenie_alert_detail`
- `opsgenie_alerts`

## Install

```bash
pip install -e plugins/opsgenie
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/opsgenie
```
