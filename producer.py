#!/usr/bin/env python3
"""
Kafka Producer Client

A simple Kafka producer that sends JSON messages to topics on the local broker.
"""

import json
import os
import sys
from threading import Lock
from confluent_kafka import Producer
from confluent_kafka import KafkaException

# Thread-safe storage for delivery errors
_delivery_errors = []
_delivery_lock = Lock()


def create_producer(bootstrap_servers=None):
    """
    Create and return a Kafka producer instance.
    
    Args:
        bootstrap_servers: Kafka broker address (default: localhost:9092)
    
    Returns:
        Producer instance configured to connect to the broker
    """
    if bootstrap_servers is None:
        bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    
    config = {
        'bootstrap.servers': bootstrap_servers,
    }
    
    try:
        producer = Producer(config)
        return producer
    except Exception as e:
        raise KafkaException(f"Failed to create producer: {e}")


def produce_message(producer, topic, value, key=None):
    """
    Produce a message to a Kafka topic.
    
    Args:
        producer: Kafka Producer instance
        topic: Topic name to send message to
        value: Message value (dict or JSON-serializable object)
        key: Optional message key (string)
    
    Returns:
        None (raises exception on failure)
    """
    try:
        # Serialize value to JSON if it's a dict or other JSON-serializable object
        if isinstance(value, dict) or not isinstance(value, (str, bytes)):
            value_json = json.dumps(value)
            value_bytes = value_json.encode('utf-8')
        elif isinstance(value, str):
            value_bytes = value.encode('utf-8')
        else:
            value_bytes = value
        
        # Encode key if provided
        key_bytes = key.encode('utf-8') if key and isinstance(key, str) else key
        
        # Produce message
        producer.produce(topic, value=value_bytes, key=key_bytes, callback=delivery_callback)
        
        # Wait for message to be delivered (flush)
        producer.poll(0)
        producer.flush()
        
    except Exception as e:
        raise KafkaException(f"Failed to produce message: {e}")


def delivery_callback(err, msg):
    """
    Callback function to handle message delivery status.
    
    Args:
        err: Error object if delivery failed, None otherwise
        msg: Message object
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
        raise KafkaException(f"Message delivery failed: {err}")
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')


def main():
    """Example usage of the producer."""
    try:
        # Create producer
        producer = create_producer()
        print("Producer created successfully")
        
        # Example: Send a message
        topic = os.getenv('KAFKA_TOPIC', 'test-topic')
        message = {
            'message': 'Hello, Kafka!',
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        print(f"Producing message to topic '{topic}': {message}")
        produce_message(producer, topic, message)
        print("Message produced successfully")
        
    except KafkaException as e:
        print(f"Kafka error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()