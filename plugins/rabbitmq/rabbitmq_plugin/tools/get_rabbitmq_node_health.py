"""Bridged tool: get_rabbitmq_node_health (from OpenSRE app.tools.RabbitMQNodeHealthTool)."""

from __future__ import annotations

from typing import Any

from rabbitmq_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_rabbitmq_node_health',
    source='rabbitmq',
    description='Return per-node RabbitMQ resource utilization: memory used vs. limit (with alarm flag), disk free vs. limit (with alarm flag), file descriptors, sockets, erlang process usage, and cluster partition state. Essential for diagnosing backpressure, partitions, or node crashes.',
    input_schema={'type': 'object', 'properties': {'management_port': {'type': 'integer'}, 'vhost': {'type': 'string'}, 'ssl': {'type': 'boolean'}, 'verify_ssl': {'type': 'boolean'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'username', 'password'),
    requires=[],
    use_cases=['Checking if a RabbitMQ node is under memory or disk pressure', 'Detecting cluster network partitions between nodes', 'Investigating file descriptor or socket exhaustion on a broker node'],
)
def get_rabbitmq_node_health(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.RabbitMQNodeHealthTool',
            attr='get_rabbitmq_node_health',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_rabbitmq_node_health failed: {exc}"}
