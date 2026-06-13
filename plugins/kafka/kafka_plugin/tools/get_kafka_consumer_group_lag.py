"""Bridged tool: get_kafka_consumer_group_lag (from OpenSRE app.tools.KafkaConsumerGroupTool)."""

from __future__ import annotations

from typing import Any

from kafka_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='get_kafka_consumer_group_lag',
    source='kafka',
    description='Retrieve consumer group lag per partition from a Kafka cluster, showing committed offsets versus high watermarks.',
    input_schema={'type': 'object', 'properties': {'group_id': {'type': 'string'}, 'security_protocol': {'type': 'string'}, 'sasl_mechanism': {'type': 'string'}}, 'required': ['group_id']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('bootstrap_servers', 'sasl_username', 'sasl_password'),
    requires=[],
    use_cases=['Diagnosing consumer lag causing processing delays', 'Identifying stuck or slow consumers during an incident', 'Checking consumer group health after a deployment'],
)
def get_kafka_consumer_group_lag(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.KafkaConsumerGroupTool',
            attr='get_kafka_consumer_group_lag',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"get_kafka_consumer_group_lag failed: {exc}"}
