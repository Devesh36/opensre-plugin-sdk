"""Bridged tool: get_rabbitmq_connection_stats (from OpenSRE app.tools.RabbitMQConnectionStatsTool)."""

from __future__ import annotations

from typing import Any

from rabbitmq_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_rabbitmq_connection_stats',
    source='rabbitmq',
    description='List active RabbitMQ connections sorted by receive rate. Reports user, vhost, protocol, channel count, peer host/port, TLS status, and recv/send byte rates — helps spot connection exhaustion, slow consumers, or noisy publishers during an incident.',
    input_schema={'type': 'object', 'properties': {'management_port': {'type': 'integer'}, 'vhost': {'type': 'string'}, 'ssl': {'type': 'boolean'}, 'verify_ssl': {'type': 'boolean'}, 'max_results': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('host', 'username', 'password'),
    requires=[],
    use_cases=['Investigating connection exhaustion or connection storms', 'Identifying noisy publishers with high byte rates', 'Checking if slow consumers are holding open idle connections'],
)
def get_rabbitmq_connection_stats(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.RabbitMQConnectionStatsTool',
            attr='get_rabbitmq_connection_stats',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_rabbitmq_connection_stats failed: {exc}"}
