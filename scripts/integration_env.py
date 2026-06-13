"""Env var gates and credential injection for bridged OpenSRE plugins."""

from __future__ import annotations

# gate: env vars — integration available when any listed var is non-empty
# inject: tool param -> env var for extract_params / injected_params
SOURCE_ENV: dict[str, dict[str, object]] = {
    "airflow": {
        "gate": ["AIRFLOW_BASE_URL"],
        "inject": {
            "base_url": "AIRFLOW_BASE_URL",
            "username": "AIRFLOW_USERNAME",
            "password": "AIRFLOW_PASSWORD",
            "auth_token": "AIRFLOW_AUTH_TOKEN",
        },
    },
    "alertmanager": {
        "gate": ["ALERTMANAGER_URL"],
        "inject": {
            "base_url": "ALERTMANAGER_URL",
            "bearer_token": "ALERTMANAGER_BEARER_TOKEN",
            "username": "ALERTMANAGER_USERNAME",
            "password": "ALERTMANAGER_PASSWORD",
        },
    },
    "argocd": {
        "gate": ["ARGOCD_BASE_URL"],
        "inject": {
            "base_url": "ARGOCD_BASE_URL",
            "auth_token": "ARGOCD_AUTH_TOKEN",
            "username": "ARGOCD_USERNAME",
            "password": "ARGOCD_PASSWORD",
        },
    },
    "aws_sdk": {
        "gate": ["AWS_ACCESS_KEY_ID", "AWS_ROLE_ARN"],
        "inject": {},
    },
    "azure": {
        "gate": ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"],
        "inject": {
            "workspace_id": "AZURE_LOG_ANALYTICS_WORKSPACE_ID",
            "token": "AZURE_LOG_ANALYTICS_TOKEN",
        },
    },
    "azure_sql": {
        "gate": ["AZURE_SQL_SERVER"],
        "inject": {
            "server": "AZURE_SQL_SERVER",
            "database": "AZURE_SQL_DATABASE",
            "username": "AZURE_SQL_USERNAME",
            "password": "AZURE_SQL_PASSWORD",
        },
    },
    "batch": {"gate": ["JWT_TOKEN", "TRACER_API_URL"], "inject": {"jwt_token": "JWT_TOKEN"}},
    "betterstack": {
        "gate": ["BETTERSTACK_QUERY_ENDPOINT"],
        "inject": {
            "endpoint": "BETTERSTACK_QUERY_ENDPOINT",
            "username": "BETTERSTACK_USERNAME",
            "password": "BETTERSTACK_PASSWORD",
        },
    },
    "bitbucket": {
        "gate": ["BITBUCKET_APP_PASSWORD", "BITBUCKET_USERNAME"],
        "inject": {
            "workspace": "BITBUCKET_WORKSPACE",
            "username": "BITBUCKET_USERNAME",
            "app_password": "BITBUCKET_APP_PASSWORD",
            "base_url": "BITBUCKET_BASE_URL",
        },
    },
    "clickhouse": {
        "gate": ["CLICKHOUSE_HOST"],
        "inject": {
            "host": "CLICKHOUSE_HOST",
            "user": "CLICKHOUSE_USER",
            "password": "CLICKHOUSE_PASSWORD",
            "database": "CLICKHOUSE_DATABASE",
        },
    },
    "cloudwatch": {"gate": ["AWS_ACCESS_KEY_ID", "AWS_ROLE_ARN"], "inject": {}},
    "coralogix": {
        "gate": ["CORALOGIX_API_KEY"],
        "inject": {
            "api_key": "CORALOGIX_API_KEY",
            "base_url": "CORALOGIX_API_URL",
        },
    },
    "dagster": {
        "gate": ["DAGSTER_ENDPOINT"],
        "inject": {"endpoint": "DAGSTER_ENDPOINT", "api_token": "DAGSTER_API_TOKEN"},
    },
    "datadog": {
        "gate": ["DD_API_KEY"],
        "inject": {
            "api_key": "DD_API_KEY",
            "app_key": "DD_APP_KEY",
            "site": "DD_SITE",
        },
    },
    "ec2": {"gate": ["AWS_ACCESS_KEY_ID", "AWS_ROLE_ARN"], "inject": {}},
    "eks": {"gate": ["AWS_ACCESS_KEY_ID", "AWS_ROLE_ARN"], "inject": {}},
    "elasticsearch": {
        "gate": ["ELASTICSEARCH_URL"],
        "inject": {
            "url": "ELASTICSEARCH_URL",
            "api_key": "ELASTICSEARCH_API_KEY",
            "username": "ELASTICSEARCH_USERNAME",
            "password": "ELASTICSEARCH_PASSWORD",
        },
    },
    "github": {
        "gate": ["GITHUB_MCP_URL", "GITHUB_MCP_COMMAND"],
        "inject": {"auth_token": "GITHUB_MCP_AUTH_TOKEN"},
    },
    "gitlab": {
        "gate": ["GITLAB_ACCESS_TOKEN"],
        "inject": {"base_url": "GITLAB_BASE_URL", "access_token": "GITLAB_ACCESS_TOKEN"},
    },
    "google_docs": {
        "gate": ["GOOGLE_CREDENTIALS_FILE"],
        "inject": {
            "credentials_file": "GOOGLE_CREDENTIALS_FILE",
            "folder_id": "GOOGLE_DRIVE_FOLDER_ID",
        },
    },
    "grafana": {
        "gate": ["GRAFANA_INSTANCE_URL"],
        "inject": {
            "url": "GRAFANA_INSTANCE_URL",
            "api_key": "GRAFANA_READ_TOKEN",
        },
    },
    "helm": {
        "gate": ["OSRE_HELM_INTEGRATION"],
        "inject": {
            "helm_path": "HELM_PATH",
            "kube_context": "HELM_KUBE_CONTEXT",
            "kubeconfig": "HELM_KUBECONFIG",
        },
    },
    "hermes": {"gate": ["HERMES_LOG_PATH", "OPENSRE_HERMES_INVESTIGATE"], "inject": {}},
    "honeycomb": {
        "gate": ["HONEYCOMB_API_KEY"],
        "inject": {
            "api_key": "HONEYCOMB_API_KEY",
            "dataset": "HONEYCOMB_DATASET",
            "base_url": "HONEYCOMB_API_URL",
        },
    },
    "incident_io": {
        "gate": ["INCIDENT_IO_API_KEY"],
        "inject": {"api_key": "INCIDENT_IO_API_KEY", "base_url": "INCIDENT_IO_BASE_URL"},
    },
    "jenkins": {
        "gate": ["JENKINS_URL"],
        "inject": {
            "url": "JENKINS_URL",
            "user": "JENKINS_USER",
            "api_token": "JENKINS_API_TOKEN",
        },
    },
    "jira": {
        "gate": ["JIRA_API_TOKEN"],
        "inject": {
            "base_url": "JIRA_BASE_URL",
            "email": "JIRA_EMAIL",
            "api_token": "JIRA_API_TOKEN",
            "project_key": "JIRA_PROJECT_KEY",
        },
    },
    "kafka": {
        "gate": ["KAFKA_BOOTSTRAP_SERVERS"],
        "inject": {
            "bootstrap_servers": "KAFKA_BOOTSTRAP_SERVERS",
            "sasl_username": "KAFKA_SASL_USERNAME",
            "sasl_password": "KAFKA_SASL_PASSWORD",
        },
    },
    "knowledge": {"gate": [], "inject": {}},
    "mariadb": {
        "gate": ["MARIADB_HOST"],
        "inject": {
            "host": "MARIADB_HOST",
            "database": "MARIADB_DATABASE",
            "username": "MARIADB_USERNAME",
            "password": "MARIADB_PASSWORD",
        },
    },
    "mongodb": {
        "gate": ["MONGODB_CONNECTION_STRING"],
        "inject": {
            "connection_string": "MONGODB_CONNECTION_STRING",
            "database": "MONGODB_DATABASE",
        },
    },
    "mongodb_atlas": {
        "gate": ["MONGODB_ATLAS_PUBLIC_KEY"],
        "inject": {
            "public_key": "MONGODB_ATLAS_PUBLIC_KEY",
            "private_key": "MONGODB_ATLAS_PRIVATE_KEY",
            "project_id": "MONGODB_ATLAS_PROJECT_ID",
        },
    },
    "mysql": {
        "gate": ["MYSQL_HOST"],
        "inject": {
            "host": "MYSQL_HOST",
            "database": "MYSQL_DATABASE",
            "username": "MYSQL_USERNAME",
            "password": "MYSQL_PASSWORD",
        },
    },
    "openclaw": {
        "gate": ["OPENCLAW_MCP_URL", "OPENCLAW_MCP_COMMAND"],
        "inject": {"auth_token": "OPENCLAW_MCP_AUTH_TOKEN"},
    },
    "openobserve": {
        "gate": ["OPENOBSERVE_URL"],
        "inject": {
            "url": "OPENOBSERVE_URL",
            "token": "OPENOBSERVE_TOKEN",
            "username": "OPENOBSERVE_USERNAME",
            "password": "OPENOBSERVE_PASSWORD",
        },
    },
    "opensearch": {
        "gate": ["OPENSEARCH_URL"],
        "inject": {
            "url": "OPENSEARCH_URL",
            "api_key": "OPENSEARCH_API_KEY",
            "username": "OPENSEARCH_USERNAME",
            "password": "OPENSEARCH_PASSWORD",
        },
    },
    "opsgenie": {
        "gate": ["OPSGENIE_API_KEY"],
        "inject": {"api_key": "OPSGENIE_API_KEY", "region": "OPSGENIE_REGION"},
    },
    "postgresql": {
        "gate": ["POSTGRESQL_HOST"],
        "inject": {
            "host": "POSTGRESQL_HOST",
            "database": "POSTGRESQL_DATABASE",
            "username": "POSTGRESQL_USERNAME",
            "password": "POSTGRESQL_PASSWORD",
        },
    },
    "prefect": {"gate": ["PREFECT_API_KEY"], "inject": {"api_key": "PREFECT_API_KEY"}},
    "rabbitmq": {
        "gate": ["RABBITMQ_HOST"],
        "inject": {
            "host": "RABBITMQ_HOST",
            "username": "RABBITMQ_USERNAME",
            "password": "RABBITMQ_PASSWORD",
        },
    },
    "rds": {
        "gate": ["AWS_ACCESS_KEY_ID", "AWS_ROLE_ARN", "RDS_DB_INSTANCE_IDENTIFIER"],
        "inject": {},
    },
    "sentry": {
        "gate": ["SENTRY_AUTH_TOKEN"],
        "inject": {
            "sentry_token": "SENTRY_AUTH_TOKEN",
            "organization_slug": "SENTRY_ORG_SLUG",
            "sentry_url": "SENTRY_URL",
            "project_slug": "SENTRY_PROJECT_SLUG",
        },
    },
    "signoz": {
        "gate": ["SIGNOZ_URL"],
        "inject": {"url": "SIGNOZ_URL", "api_key": "SIGNOZ_API_KEY"},
    },
    "snowflake": {
        "gate": ["SNOWFLAKE_TOKEN", "SNOWFLAKE_ACCOUNT"],
        "inject": {
            "token": "SNOWFLAKE_TOKEN",
            "account": "SNOWFLAKE_ACCOUNT_IDENTIFIER",
        },
    },
    "splunk": {
        "gate": ["SPLUNK_URL"],
        "inject": {"url": "SPLUNK_URL", "token": "SPLUNK_TOKEN"},
    },
    "storage": {"gate": ["AWS_ACCESS_KEY_ID", "AWS_ROLE_ARN"], "inject": {}},
    "supabase": {
        "gate": ["SUPABASE_URL"],
        "inject": {"url": "SUPABASE_URL", "service_key": "SUPABASE_SERVICE_KEY"},
    },
    "tracer_web": {
        "gate": ["JWT_TOKEN", "TRACER_API_URL"],
        "inject": {"jwt_token": "JWT_TOKEN", "api_url": "TRACER_API_URL"},
    },
    "twilio": {
        "gate": ["TWILIO_ACCOUNT_SID"],
        "inject": {
            "account_sid": "TWILIO_ACCOUNT_SID",
            "auth_token": "TWILIO_AUTH_TOKEN",
        },
    },
    "vercel": {
        "gate": ["VERCEL_API_TOKEN"],
        "inject": {"api_token": "VERCEL_API_TOKEN", "team_id": "VERCEL_TEAM_ID"},
    },
    "victoria_logs": {
        "gate": ["VICTORIA_LOGS_URL"],
        "inject": {"url": "VICTORIA_LOGS_URL", "tenant_id": "VICTORIA_LOGS_TENANT_ID"},
    },
}

CREDENTIAL_PARAM_HINTS = frozenset(
    {
        "api_token",
        "api_key",
        "app_key",
        "auth_token",
        "token",
        "password",
        "bearer_token",
        "sentry_token",
        "access_token",
        "app_password",
        "service_key",
        "private_key",
        "connection_string",
        "credentials_file",
        "jwt_token",
    }
)

SKIP_SOURCES = frozenset()  # native plugins use different slugs (linear, mock)

NATIVE_PLUGINS = frozenset({"linear", "mock"})
