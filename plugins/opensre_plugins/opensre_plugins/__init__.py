"""Register bundled OpenSRE integration plugins from one entry point."""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module

PLUGIN_REGISTRARS: dict[str, str] = {
    "airflow": "airflow_plugin:register",
    "alertmanager": "alertmanager_plugin:register",
    "argocd": "argocd_plugin:register",
    "aws_sdk": "aws_sdk_plugin:register",
    "azure": "azure_plugin:register",
    "azure_sql": "azure_sql_plugin:register",
    "batch": "batch_plugin:register",
    "betterstack": "betterstack_plugin:register",
    "bitbucket": "bitbucket_plugin:register",
    "clickhouse": "clickhouse_plugin:register",
    "cloudwatch": "cloudwatch_plugin:register",
    "coralogix": "coralogix_plugin:register",
    "dagster": "dagster_plugin:register",
    "datadog": "datadog_plugin:register",
    "ec2": "ec2_plugin:register",
    "eks": "eks_plugin:register",
    "elasticsearch": "elasticsearch_plugin:register",
    "github": "github_plugin:register",
    "gitlab": "gitlab_plugin:register",
    "google_docs": "google_docs_plugin:register",
    "grafana": "grafana_plugin:register",
    "helm": "helm_plugin:register",
    "hermes": "hermes_plugin:register",
    "honeycomb": "honeycomb_plugin:register",
    "incident_io": "incident_io_plugin:register",
    "jenkins": "jenkins_plugin:register",
    "jira": "jira_plugin:register",
    "kafka": "kafka_plugin:register",
    "knowledge": "knowledge_plugin:register",
    "linear": "linear_plugin:register",
    "mariadb": "mariadb_plugin:register",
    "mock": "mock_plugin:register",
    "mongodb": "mongodb_plugin:register",
    "mongodb_atlas": "mongodb_atlas_plugin:register",
    "mysql": "mysql_plugin:register",
    "openclaw": "openclaw_plugin:register",
    "openobserve": "openobserve_plugin:register",
    "opensearch": "opensearch_plugin:register",
    "opsgenie": "opsgenie_plugin:register",
    "postgresql": "postgresql_plugin:register",
    "prefect": "prefect_plugin:register",
    "rabbitmq": "rabbitmq_plugin:register",
    "rds": "rds_plugin:register",
    "sentry": "sentry_plugin:register",
    "signoz": "signoz_plugin:register",
    "snowflake": "snowflake_plugin:register",
    "splunk": "splunk_plugin:register",
    "storage": "storage_plugin:register",
    "supabase": "supabase_plugin:register",
    "tracer_web": "tracer_web_plugin:register",
    "twilio": "twilio_plugin:register",
    "vercel": "vercel_plugin:register",
    "victoria_logs": "victoria_logs_plugin:register",
}


def list_plugins() -> list[str]:
    """Return names of plugins known to this bundle."""
    return sorted(PLUGIN_REGISTRARS)


def _resolve_register(entry: str) -> Callable[[], None]:
    module_path, func_name = entry.split(":", 1)
    module = import_module(module_path)
    register = getattr(module, func_name, None)
    if register is None or not callable(register):
        raise TypeError(f"{entry!r} is not a callable register() entry point")
    return register


def register_all(
    *,
    only: list[str] | None = None,
    skip_missing: bool = True,
) -> list[str]:
    """Register every installed plugin in this bundle.

    Returns the plugin names that were registered successfully.
    Skips plugins that are not installed when *skip_missing* is True.
    """
    registered: list[str] = []
    for name, entry in PLUGIN_REGISTRARS.items():
        if only is not None and name not in only:
            continue
        try:
            _resolve_register(entry)()
        except ImportError:
            if not skip_missing:
                raise
            continue
        registered.append(name)
    return registered
