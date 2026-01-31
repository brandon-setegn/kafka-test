#!/usr/bin/env python3
"""
Kafka Consumer Client

A simple Kafka consumer that reads JSON messages from topics on the local broker.
Uses Kafka message timestamp (CreateTime/LogAppendTime) for when the message was produced.
"""

import json
import os
import sys
from datetime import datetime
from confluent_kafka import Consumer
from confluent_kafka import KafkaException, KafkaError


def create_consumer(bootstrap_servers=None, group_id=None):
    """
    Create and return a Kafka consumer instance.
    
    Args:
        bootstrap_servers: Kafka broker address (default: localhost:9092)
        group_id: Consumer group ID (default: python-consumer-group)
    
    Returns:
        Consumer instance configured to connect to the broker
    """
    if bootstrap_servers is None:
        bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    
    if group_id is None:
        group_id = os.getenv('KAFKA_CONSUMER_GROUP', 'python-consumer-group')
    
    config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',  # Start from beginning if no offset exists
    }
    
    try:
        consumer = Consumer(config)
        return consumer
    except Exception as e:
        raise KafkaException(f"Failed to create consumer: {e}")


def consume_messages(consumer, topics, timeout=1.0, max_messages=None):
    """
    Consume messages from Kafka topics.
    
    Args:
        consumer: Kafka Consumer instance
        topics: List of topic names to subscribe to, or single topic name
        timeout: Timeout in seconds for polling (default: 1.0)
        max_messages: Maximum number of messages to consume (None for unlimited)
    
    Yields:
        Tuple of (topic, partition, offset, timestamp_ms, deserialized_message_dict).
        timestamp_ms is from Kafka (CreateTime or LogAppendTime), or None if not available.
    """
    # Convert single topic to list
    if isinstance(topics, str):
        topics = [topics]
    
    try:
        # Subscribe to topics
        consumer.subscribe(topics)
        print(f"Subscribed to topics: {topics}")
        
        message_count = 0
        
        while True:
            # Check if we've reached max messages
            if max_messages is not None and message_count >= max_messages:
                break
            
            # Poll for messages
            msg = consumer.poll(timeout=timeout)
            
            if msg is None:
                continue
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event (not an error)
                    continue
                else:
                    raise KafkaException(f"Consumer error: {msg.error()}")
            
            # Deserialize message value from JSON
            # Handle tombstone messages (None value)
            msg_value = msg.value()
            if msg_value is None:
                # Tombstone message (null value)
                value_dict = None
            else:
                try:
                    value_str = msg_value.decode('utf-8')
                    value_dict = json.loads(value_str)
                except (UnicodeDecodeError, json.JSONDecodeError, AttributeError) as e:
                    # If not JSON or decode fails, return as string
                    try:
                        value_dict = {'raw_value': msg_value.decode('utf-8', errors='replace')}
                    except AttributeError:
                        # Fallback if value is not bytes-like
                        value_dict = {'raw_value': str(msg_value)}
            
            message_count += 1
            
            # Kafka timestamp: (timestamp_type, timestamp_ms); type 1=CreateTime, 2=LogAppendTime
            ts_type, ts_ms = msg.timestamp()
            timestamp_ms = ts_ms if ts_type else None
            
            yield (msg.topic(), msg.partition(), msg.offset(), timestamp_ms, value_dict)
            
    except KeyboardInterrupt:
        print("\nConsumer interrupted by user")
    except KafkaException as e:
        raise
    finally:
        consumer.close()


def main():
    """Example usage of the consumer."""
    try:
        # Create consumer
        consumer = create_consumer()
        print("Consumer created successfully")
        
        # Example: Consume messages
        topic = os.getenv('KAFKA_TOPIC', 'test-topic')
        print(f"Consuming messages from topic '{topic}'...")
        print("Press Ctrl+C to stop\n")
        
        for topic_name, partition, offset, timestamp_ms, message in consume_messages(consumer, topic, max_messages=10):
            ts_str = ""
            if timestamp_ms is not None:
                dt = datetime.fromtimestamp(timestamp_ms / 1000.0)  # local time
                ts_str = f" (produced: {dt.strftime('%b %d, %Y at %I:%M:%S %p')})"
            print(f"Received message from {topic_name}[{partition}] at offset {offset}{ts_str}:")
            print(f"  {json.dumps(message, indent=2)}")
            print()
        
        print("Finished consuming messages")
        
    except KafkaException as e:
        print(f"Kafka error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()