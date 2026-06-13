"""Bridged tool: get_rabbitmq_broker_overview (from OpenSRE app.tools.RabbitMQBrokerOverviewTool)."""

from __future__ import annotations

from typing import Any

from rabbitmq_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_rabbitmq_broker_overview',
    source='rabbitmq',
    description='Return a cluster-wide RabbitMQ overview: version, cluster name, total message counts, publish/deliver rates, queue/consumer/connection/channel totals, plus the alarm health-check status (memory / disk / file-descriptor alarms).',
    input_schema={'type': 'object', 'properties': {'management_port': {'type': 'integer'}, 'vhost': {'type': 'string'}, 'ssl': {'type': 'boolean'}, 'verify_ssl': {'type': 'boolean'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'username', 'password'),
    requires=[],
    use_cases=['Getting a quick cluster-wide health snapshot during an incident', 'Checking if memory or disk alarms are active on the broker', 'Comparing publish vs deliver rates to detect throughput imbalances'],
)
def get_rabbitmq_broker_overview(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.RabbitMQBrokerOverviewTool',
            attr='get_rabbitmq_broker_overview',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_rabbitmq_broker_overview failed: {exc}"}
