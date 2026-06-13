# opensre-plugin-incident-io

Bridged OpenSRE **incident_io** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `INCIDENT_IO_API_KEY`

## Tools

- `incident_io_incidents`

## Install

```bash
pip install -e plugins/incident_io
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/incident_io
```
