"""Kafka producer and consumer for event streaming."""

import json
from typing import Optional

from kafka import KafkaProducer, KafkaConsumer


def create_producer(bootstrap_servers: str = "localhost:9092") -> KafkaProducer:
    """Create Kafka producer for publishing events."""
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def create_consumer(
    topic: str,
    bootstrap_servers: str = "localhost:9092",
    group_id: Optional[str] = "devtools-consumer",
) -> KafkaConsumer:
    """Create Kafka consumer for consuming events."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )


def produce_message(producer: KafkaProducer, topic: str, message: dict) -> None:
    """Send message to Kafka topic."""
    producer.send(topic, value=message)
    producer.flush()
