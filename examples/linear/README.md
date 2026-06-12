# opensre-plugin-linear

Reference OpenSRE plugin that searches Linear issues via the GraphQL API.

## Setup

```bash
pip install -e examples/linear
pip install -e .  # SDK
export LINEAR_API_KEY=lin_api_xxx
opensre-plugin validate examples/linear
python -c "from linear_plugin import register; register()"
opensre investigate --alert '...'
```

Tools are gated on `LINEAR_API_KEY` — no OpenSRE core changes required.
