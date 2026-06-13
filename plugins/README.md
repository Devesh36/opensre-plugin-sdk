# OpenSRE integration plugins

All OpenSRE investigation integrations live here as external plugin packages. Core OpenSRE keeps the agent loop; this repo owns integration tooling.

## Layout

```text
plugins/
├── linear/              # Native — Linear GraphQL (LINEAR_API_KEY)
├── mock/                # Native — offline demo (MOCK_API_KEY)
├── vercel/              # Bridged — 2 tools
├── sentry/              # Bridged — 3 tools
├── datadog/             # Bridged — 6 tools
├── …                    # 51 integrations total (see table below)
└── opensre_plugins/     # Meta package — register_all()
```

**Native plugins** (`linear`, `mock`) ship standalone client code.

**Bridged plugins** (everything else) register tools via `opensre-plugin-sdk` and delegate execution to OpenSRE core (`pip install opensre`). Env-based `is_available` / `extract_params` work without the integration catalog. Port client code into each plugin over time to drop the `opensre` runtime dependency.

## Quick start

```bash
uv sync --extra dev
uv pip install -e . -e plugins/opensre_plugins -e plugins/vercel -e plugins/sentry
pip install opensre   # required for bridged tool execution

export VERCEL_API_TOKEN=xxx
export SENTRY_AUTH_TOKEN=xxx
export SENTRY_ORG_SLUG=my-org

python -c "from opensre_plugins import register_all; print(register_all(only=['vercel','sentry']))"
opensre investigate --alert '{"title": "Production incident"}'
```

Validate every plugin offline:

```bash
uv run python scripts/validate_all_plugins.py
```

Regenerate bridged plugins from a local OpenSRE checkout:

```bash
cd ../opensre && uv run python ../opensre-sdk/scripts/export_tool_inventory.py
cd ../opensre-sdk && uv run python scripts/generate_opensre_plugins.py
```

## All plugins (53)

| Plugin | Tools | Type | Primary env vars |
|--------|------:|------|------------------|
| airflow | 3 | bridged | `AIRFLOW_BASE_URL` |
| alertmanager | 2 | bridged | `ALERTMANAGER_URL` |
| argocd | 2 | bridged | `ARGOCD_BASE_URL` |
| aws_sdk | 1 | bridged | `AWS_ACCESS_KEY_ID` / `AWS_ROLE_ARN` |
| azure | 1 | bridged | `AZURE_LOG_ANALYTICS_WORKSPACE_ID` |
| azure_sql | 5 | bridged | `AZURE_SQL_SERVER` |
| batch | 1 | bridged | `JWT_TOKEN`, `TRACER_API_URL` |
| betterstack | 1 | bridged | `BETTERSTACK_QUERY_ENDPOINT` |
| bitbucket | 3 | bridged | `BITBUCKET_APP_PASSWORD` |
| clickhouse | 2 | bridged | `CLICKHOUSE_HOST` |
| cloudwatch | 8 | bridged | `AWS_ACCESS_KEY_ID` / `AWS_ROLE_ARN` |
| coralogix | 1 | bridged | `CORALOGIX_API_KEY` |
| dagster | 5 | bridged | `DAGSTER_ENDPOINT` |
| datadog | 6 | bridged | `DD_API_KEY` |
| ec2 | 2 | bridged | `AWS_ACCESS_KEY_ID` / `AWS_ROLE_ARN` |
| eks | 11 | bridged | `AWS_ACCESS_KEY_ID` / `AWS_ROLE_ARN` |
| elasticsearch | 1 | bridged | `ELASTICSEARCH_URL` |
| github | 9 | bridged | `GITHUB_MCP_URL` / `GITHUB_MCP_COMMAND` |
| gitlab | 4 | bridged | `GITLAB_ACCESS_TOKEN` |
| google_docs | 1 | bridged | `GOOGLE_CREDENTIALS_FILE` |
| grafana | 5 | bridged | `GRAFANA_INSTANCE_URL` |
| helm | 5 | bridged | `OSRE_HELM_INTEGRATION` |
| hermes | 19 | bridged | `HERMES_LOG_PATH` |
| honeycomb | 1 | bridged | `HONEYCOMB_API_KEY` |
| incident_io | 1 | bridged | `INCIDENT_IO_API_KEY` |
| jenkins | 5 | bridged | `JENKINS_URL` |
| jira | 4 | bridged | `JIRA_API_TOKEN` |
| kafka | 2 | bridged | `KAFKA_BOOTSTRAP_SERVERS` |
| knowledge | 2 | bridged | none |
| **linear** | 1 | **native** | `LINEAR_API_KEY` |
| mariadb | 5 | bridged | `MARIADB_HOST` |
| **mock** | 1 | **native** | `MOCK_API_KEY` |
| mongodb | 5 | bridged | `MONGODB_CONNECTION_STRING` |
| mongodb_atlas | 5 | bridged | `MONGODB_ATLAS_PUBLIC_KEY` |
| mysql | 5 | bridged | `MYSQL_HOST` |
| openclaw | 5 | bridged | `OPENCLAW_MCP_URL` |
| openobserve | 1 | bridged | `OPENOBSERVE_URL` |
| opensearch | 1 | bridged | `OPENSEARCH_URL` |
| opsgenie | 2 | bridged | `OPSGENIE_API_KEY` |
| postgresql | 5 | bridged | `POSTGRESQL_HOST` |
| prefect | 2 | bridged | `PREFECT_API_KEY` |
| rabbitmq | 5 | bridged | `RABBITMQ_HOST` |
| rds | 2 | bridged | `RDS_DB_INSTANCE_IDENTIFIER` |
| sentry | 3 | bridged | `SENTRY_AUTH_TOKEN` |
| signoz | 3 | bridged | `SIGNOZ_URL` |
| snowflake | 1 | bridged | `SNOWFLAKE_TOKEN` |
| splunk | 1 | bridged | `SPLUNK_URL` |
| storage | 4 | bridged | `AWS_ACCESS_KEY_ID` / `AWS_ROLE_ARN` |
| supabase | 2 | bridged | `SUPABASE_URL` |
| tracer_web | 7 | bridged | `JWT_TOKEN`, `TRACER_API_URL` |
| twilio | 1 | bridged | `TWILIO_ACCOUNT_SID` |
| vercel | 2 | bridged | `VERCEL_API_TOKEN` |
| victoria_logs | 1 | bridged | `VICTORIA_LOGS_URL` |

## Add a new integration

1. Add the tool(s) in OpenSRE core (or author natively here like `linear`).
2. Re-run `export_tool_inventory.py` + `generate_opensre_plugins.py`, or scaffold with `opensre-plugin init myvendor`.
3. Add env mapping in `scripts/integration_env.py` if needed.
4. Register in `plugins/opensre_plugins/opensre_plugins/__init__.py` (auto-updated by the generator).

See [docs/AUTHORING.md](../docs/AUTHORING.md) and [docs/PHASE1_VS_PHASE2.md](../docs/PHASE1_VS_PHASE2.md).
