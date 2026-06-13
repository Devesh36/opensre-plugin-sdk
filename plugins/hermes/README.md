# opensre-plugin-hermes

Bridged OpenSRE **hermes** integration (19 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `HERMES_LOG_PATH`
- `OPENSRE_HERMES_INVESTIGATE`

## Tools

- `get_hermes_adapter_catalog`
- `get_hermes_approval_events`
- `get_hermes_audit_trail`
- `get_hermes_config`
- `get_hermes_credential_state`
- `get_hermes_cron_state`
- `get_hermes_filesystem_state`
- `get_hermes_kv_cache_state`
- `get_hermes_logs`
- `get_hermes_memory_state`
- `get_hermes_message_history`
- `get_hermes_orchestration_state`
- `get_hermes_provider_traffic`
- `get_hermes_rbac_state`
- `get_hermes_routing_decisions`
- `get_hermes_runtime_state`
- `get_hermes_session_log`
- `get_hermes_session_topology`
- `get_hermes_workflow_run`

## Install

```bash
pip install -e plugins/hermes
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/hermes
```
