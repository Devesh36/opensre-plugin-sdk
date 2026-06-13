# FAQ

## Do I need a new repo per plugin?

**No.** The SDK validates Python **packages**, not GitHub repo count. Both layouts work:

### Separate repo (one plugin per repo)

Best when a plugin is maintained by a different team or release cadence.

```text
github.com/you/opensre-plugin-linear/
  linear_plugin/
  pyproject.toml
```

Install:

```bash
pip install "opensre-plugin-linear @ git+https://github.com/you/opensre-plugin-linear.git"
```

### Monorepo (multiple plugins)

Best for a personal or org plugin collection.

```text
opensre-community-plugins/
  plugins/
    linear/
      linear_plugin/
      pyproject.toml
    splunk/
      splunk_plugin/
      pyproject.toml
```

Each plugin has its own `pyproject.toml` with `[tool.opensre-plugin]`. Install individually:

```bash
pip install -e plugins/linear
pip install -e plugins/splunk
```

Register each:

```python
from linear_plugin import register as register_linear
from splunk_plugin import register as register_splunk

register_linear()
register_splunk()
```

### This SDK repo

`plugins/linear` and `plugins/mock` live in the same repo as the SDK — that's the bundled integrations monorepo.

---

## Do I need to fork OpenSRE?

No. Phase 1 plugins run in-process via `register_external_tool_package()`. Install `opensre` and your plugin as dependencies.

## Does `opensre-plugin validate` need OpenSRE installed?

No. Schema and manifest checks run offline. `@plugin_tool` attaches offline stubs when OpenSRE isn't installed.

Registration (`register_tools`, `opensre-plugin register`) **does** require OpenSRE.

## Why must tools live in `tools/*.py` files?

OpenSRE's registry walks **submodules** of the registered package (same as `app.tools.*`). A tool defined only in `tools/__init__.py` is not discovered. Put each `@plugin_tool` in its own file under `tools/`.

## Why did my investigation break after adding a plugin?

One invalid tool schema breaks **all** investigations. Run `opensre-plugin validate` before `register()`. The SDK validates before calling `register_external_tool_package()` so invalid plugins cannot pollute the registry.

## Can I add a new `EvidenceSource` like `"linear"`?

Not in Phase 1 without a core PR to `app/types/evidence.py`. Reuse the closest existing source (e.g. `"github"` for issue trackers) until Phase 2.

## How do I ship API keys securely?

Use `injected_params` + `extract_params`. Never put secrets in `input_schema`. See [AUTHORING.md](AUTHORING.md).

## When should I open the upstream docs PR?

After an OpenSRE maintainer says the SDK looks good. Templates are in [`docs/upstream-pr/`](upstream-pr/) — do not open preemptively.

## Where is PyPI?

Install from GitHub until `PYPI_API_TOKEN` is configured and a release publishes:

```bash
pip install "opensre-plugin-sdk @ git+https://github.com/Devesh36/opensre-plugin-sdk.git@v0.1.0"
```
