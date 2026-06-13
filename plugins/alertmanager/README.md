# opensre-plugin-alertmanager

Bridged OpenSRE **alertmanager** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `ALERTMANAGER_URL`

## Tools

- `alertmanager_alerts`
- `alertmanager_silences`

## Install

```bash
pip install -e plugins/alertmanager
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/alertmanager
```
