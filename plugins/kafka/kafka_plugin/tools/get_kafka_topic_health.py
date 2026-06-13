"""Bridged tool: get_kafka_topic_health (from OpenSRE app.tools.KafkaTopicHealthTool)."""

from __future__ import annotations

from typing import Any

from kafka_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_kafka_topic_health',
    source='kafka',
    description='Retrieve topic partition health from a Kafka cluster, including replica status, ISR counts, and under-replicated partitions.',
    input_schema={'type': 'object', 'properties': {'topic': {'type': 'string'}, 'security_protocol': {'type': 'string'}, 'sasl_mechanism': {'type': 'string'}, 'limit': {'type': 'integer'}}},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('bootstrap_servers', 'sasl_username', 'sasl_password'),
    requires=[],
    use_cases=['Checking partition health during a consumer lag incident', 'Identifying under-replicated partitions after a broker failure', 'Reviewing topic metadata for capacity planning'],
)
def get_kafka_topic_health(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.KafkaTopicHealthTool',
            attr='get_kafka_topic_health',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_kafka_topic_health failed: {exc}"}
