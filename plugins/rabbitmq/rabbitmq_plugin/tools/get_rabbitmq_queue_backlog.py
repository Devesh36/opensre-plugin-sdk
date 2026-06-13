"""Bridged tool: get_rabbitmq_queue_backlog (from OpenSRE app.tools.RabbitMQQueueBacklogTool)."""

from __future__ import annotations

from typing import Any

from rabbitmq_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_rabbitmq_queue_backlog',
    source='rabbitmq',
    description='List RabbitMQ queues ranked by backlog size (unacknowledged + ready messages). Reveals which queues are accumulating messages, their consumer count, and publish/deliver/ack rates.',
    input_schema={'type': 'object', 'properties': {'management_port': {'type': 'integer'}, 'vhost': {'type': 'string'}, 'ssl': {'type': 'boolean'}, 'verify_ssl': {'type': 'boolean'}, 'max_results': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'username', 'password'),
    requires=[],
    use_cases=['Identifying queues with growing backlogs during an incident', 'Checking if consumers are keeping up with publish rate', 'Finding queues with zero consumers that are silently accumulating messages'],
)
def get_rabbitmq_queue_backlog(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.RabbitMQQueueBacklogTool',
            attr='get_rabbitmq_queue_backlog',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_rabbitmq_queue_backlog failed: {exc}"}
