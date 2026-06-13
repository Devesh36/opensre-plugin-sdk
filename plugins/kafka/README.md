# opensre-plugin-kafka

Bridged OpenSRE **kafka** integration (2 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `KAFKA_BOOTSTRAP_SERVERS`

## Tools

- `get_kafka_consumer_group_lag`
- `get_kafka_topic_health`

## Install

```bash
pip install -e plugins/kafka
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/kafka
```
