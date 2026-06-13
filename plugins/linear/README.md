# opensre-plugin-linear

Reference OpenSRE plugin that searches Linear issues via the GraphQL API. Demonstrates the full external plugin pattern without any OpenSRE core changes.

## Prerequisites

- Python 3.12+
- [opensre-plugin-sdk](https://github.com/Devesh36/opensre-plugin-sdk)
- [OpenSRE](https://github.com/Tracer-Cloud/opensre) (for registration and `opensre investigate`)
- A [Linear API key](https://linear.app/settings/api) (`LINEAR_API_KEY`)

## 1. Install the SDK and plugin

From anywhere:

```bash
pip install "opensre-plugin-sdk @ git+https://github.com/Devesh36/opensre-plugin-sdk.git@v0.1.0"
git clone https://github.com/Devesh36/opensre-plugin-sdk.git
cd opensre-plugin-sdk
pip install -e plugins/linear
```

Or from an already-cloned SDK repo:

```bash
pip install -e .                    # SDK
pip install -e plugins/linear      # this plugin
```

## 2. Validate offline (no OpenSRE, no API key)

```bash
opensre-plugin validate plugins/linear
```

Expected:

```text
OK: plugin 'linear' (1 tool(s))
  - search_linear_issues
```

## 3. Configure credentials

```bash
export LINEAR_API_KEY=lin_api_xxxxxxxx
```

The tool is gated on this env var via `is_available` / `extract_params` — no `_catalog_impl.py` changes.

## 4. Install OpenSRE

```bash
pip install "opensre @ git+https://github.com/Tracer-Cloud/opensre.git"
# or: pip install opensre   # when published to PyPI
```

Configure your LLM provider per [OpenSRE docs](https://github.com/Tracer-Cloud/opensre) (e.g. `LLM_PROVIDER`, API keys).

## 5. Register the plugin

```bash
python -c "from linear_plugin import register; register()"
```

Or via CLI:

```bash
opensre-plugin register plugins/linear
```

Verify:

```bash
python -c "
from app.tools.registry import get_registered_tools
names = [t.name for t in get_registered_tools('investigation')]
print('search_linear_issues' in names)
"
```

## 6. Run an investigation

```bash
opensre investigate --alert '{
  "title": "Payment API 500 errors",
  "annotations": {
    "context_sources": "github",
    "service": "payment-api"
  }
}'
```

The agent may call `search_linear_issues` when Linear is relevant to the alert.

## 7. Test the tool directly

```bash
export LINEAR_API_KEY=lin_api_xxxxxxxx
python -c "
from linear_plugin.tools.search_issues import search_linear_issues
print(search_linear_issues(query='payment outage', api_key='$LINEAR_API_KEY'))
"
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Tool not in registry | Call `register()` in the same Python process before `opensre investigate` |
| `search_linear_issues` not available | Set `LINEAR_API_KEY` |
| Schema validation fails | Run `opensre-plugin validate plugins/linear` and fix reported paths |
| 401 from Linear | Check API key permissions |

## Offline alternative

For demos without a Linear account, use [`plugins/mock`](../mock/) instead.
