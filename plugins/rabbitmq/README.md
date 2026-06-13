# opensre-plugin-rabbitmq

Bridged OpenSRE **rabbitmq** integration (5 tool(s)).
Tool implementations delegate to `opensre` core until fully ported.

## Env vars

- `RABBITMQ_HOST`

## Tools

- `get_rabbitmq_broker_overview`
- `get_rabbitmq_connection_stats`
- `get_rabbitmq_consumer_health`
- `get_rabbitmq_node_health`
- `get_rabbitmq_queue_backlog`

## Install

```bash
pip install -e plugins/rabbitmq
pip install opensre  # required for bridged tool execution
```

## Validate

```bash
opensre-plugin validate plugins/rabbitmq
```
