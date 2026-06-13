# opensre-plugin-google-docs

Bridged OpenSRE **google_docs** integration (1 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `GOOGLE_CREDENTIALS_FILE`

## Tools

- `create_google_docs_incident_report`

## Install

```bash
pip install -e plugins/google_docs
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/google_docs
```
