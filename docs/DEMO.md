# Demo transcript

Recorded output from `scripts/demo_e2e.py` and manual CLI checks. Proves validate → register → tool run without a live maintainer pitch.

## End-to-end smoke test (`scripts/demo_e2e.py`)

```bash
uv pip install -e ../opensre   # once
uv run python scripts/demo_e2e.py
```

```
1/4  opensre-plugin validate examples/linear
OK: plugin 'linear' (1 tool(s))
  - search_linear_issues

2/4  Schema check on linear_plugin.tools
  OK: search_linear_issues schema valid

3/4  register_tools(linear_plugin.tools)
  OK: registered 'search_linear_issues' (source=github)

4/4  Tool availability + dry run
  OK: run() returned error payload (expected without real API): Linear API request failed: Client error '401 Unauthorized' for url 'https://api.

Demo complete. To run a full investigation:
  export LINEAR_API_KEY=lin_api_xxx
  python -c "from linear_plugin import register; register()"
  opensre investigate --alert '{"title": "Payment API 500 errors"}'
```

## Mock plugin (offline, no network)

```bash
opensre-plugin validate examples/mock
```

```
OK: plugin 'mock' (1 tool(s))
  - search_mock_records
```

```bash
export MOCK_API_KEY=demo
python -c "
from mock_plugin.tools.search_records import search_mock_records
print(search_mock_records(query='payment outage', api_key='demo'))
"
```

```
{'success': True, 'records': [{'id': 'mock-1', 'title': 'Mock record matching: payment outage'}]}
```

## Schema validation error (main value prop)

Invalid schema with `"type": ["string", "null"]`:

```bash
opensre-plugin validate /path/to/bad_plugin
```

```
Validation failed for plugin 'bad':
  - tool 'bad_tool' at 'properties.x.type': type must not be a list ['string', 'null']
```

## Scaffold + validate (`opensre-plugin init`)

```bash
opensre-plugin init foo --output /tmp
opensre-plugin validate /tmp/foo_plugin
```

```
OK: plugin 'foo' (1 tool(s))
  - search_foo
```

## Terminal recording for GitHub Release

```bash
./scripts/record_demo.sh
# or: asciinema rec demo.cast ./scripts/record_demo.sh
```

Attach `demo.cast` or a screen recording to the [v0.1.0 release](https://github.com/Devesh36/opensre-plugin-sdk/releases/tag/v0.1.0).
