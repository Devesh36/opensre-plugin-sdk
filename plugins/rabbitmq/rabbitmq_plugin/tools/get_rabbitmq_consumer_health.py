"""Bridged tool: get_rabbitmq_consumer_health (from OpenSRE app.tools.RabbitMQConsumerHealthTool)."""

from __future__ import annotations

from typing import Any

from rabbitmq_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_rabbitmq_consumer_health',
    source='rabbitmq',
    description='List active RabbitMQ consumers with per-queue diagnostics: prefetch count, ack mode, active state, and the channel/connection each consumer is bound to. Helps identify stalled or missing consumers behind a backlog.',
    input_schema={'type': 'object', 'properties': {'management_port': {'type': 'integer'}, 'vhost': {'type': 'string'}, 'ssl': {'type': 'boolean'}, 'verify_ssl': {'type': 'boolean'}, 'max_results': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'username', 'password'),
    requires=[],
    use_cases=['Diagnosing why a queue backlog is growing — are consumers connected?', 'Checking prefetch counts to see if consumers are throttled', 'Identifying stalled or inactive consumers on a specific queue'],
)
def get_rabbitmq_consumer_health(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.RabbitMQConsumerHealthTool',
            attr='get_rabbitmq_consumer_health',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_rabbitmq_consumer_health failed: {exc}"}
