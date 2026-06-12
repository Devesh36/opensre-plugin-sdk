# opensre-plugin-mock

Offline reference plugin — no real API keys or network calls. Use this to prove the SDK works without Linear or any vendor integration.

## Prerequisites

- Python 3.12+
- [opensre-plugin-sdk](https://github.com/Devesh36/opensre-plugin-sdk) installed
- Optional: [OpenSRE](https://github.com/Tracer-Cloud/opensre) for registration tests

## Install

From the SDK repo root:

```bash
pip install "opensre-plugin-sdk @ git+https://github.com/Devesh36/opensre-plugin-sdk.git@v0.1.0"
pip install -e examples/mock
```

## Validate (offline — no OpenSRE required)

```bash
opensre-plugin validate examples/mock
```

Expected output:

```text
OK: plugin 'mock' (1 tool(s))
  - search_mock_records
```

## Register with OpenSRE

```bash
pip install opensre   # or: pip install "opensre @ git+https://github.com/Tracer-Cloud/opensre.git"
export MOCK_API_KEY=demo   # any non-empty value enables the tool
python -c "from mock_plugin import register; register()"
```

Verify the tool appears:

```bash
python -c "
from app.tools.registry import get_registered_tools
print([t.name for t in get_registered_tools('investigation') if 'mock' in t.name])
"
```

## Run the tool directly

```bash
export MOCK_API_KEY=demo
python -c "
from mock_plugin.tools.search_records import search_mock_records
print(search_mock_records(query='payment outage', api_key='demo'))
"
```

Expected:

```json
{"success": true, "records": [{"id": "mock-1", "title": "Mock record matching: payment outage"}]}
```

## How it differs from Linear

| | `examples/mock` | `examples/linear` |
|---|-----------------|-------------------|
| API | In-memory stub | Linear GraphQL |
| Network | None | HTTPS |
| Env var | `MOCK_API_KEY` | `LINEAR_API_KEY` |
| Best for | CI, demos, learning | Real integration pattern |
