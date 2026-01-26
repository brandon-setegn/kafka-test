## Context
This change adds Python-based Kafka producer and consumer clients to interact with the local Kafka broker. The implementation should be straightforward, well-documented, and suitable for learning and experimentation with Kafka concepts.

## Goals / Non-Goals
- **Goals**:
  - Provide working Python examples for producing and consuming Kafka messages
  - Use a reliable, well-maintained Python Kafka library
  - Keep code simple and easy to understand for learning purposes
  - Connect to the existing local Kafka broker (localhost:9092)
  - Support basic message production and consumption operations
  
- **Non-Goals**:
  - Advanced Kafka features (transactions, exactly-once semantics, etc.)
  - Schema Registry integration (can be added later if needed)
  - Production-ready error handling and monitoring (this is for local development/testing)
  - Multiple consumer group patterns (basic consumer group support is sufficient)
  - Custom serialization formats beyond JSON (can be extended later)

## Decisions
- **Decision**: Use `confluent-kafka` Python library
  - **Rationale**: 
    - Official Confluent library with excellent performance (C-based)
    - Well-documented and widely used
    - Actively maintained
    - Supports both producer and consumer patterns
  - **Alternatives considered**: 
    - `kafka-python` (pure Python, easier to install but slower performance)
    - `aiokafka` (async support, but adds complexity for basic use cases)

- **Decision**: Use JSON for message serialization
  - **Rationale**: Simple, human-readable format suitable for testing and experimentation
  - **Alternatives considered**: 
    - Avro (requires Schema Registry, adds complexity)
    - Protobuf (requires schema definitions, more complex)
    - Plain strings (less structured, harder to work with)

- **Decision**: Separate producer.py and consumer.py files
  - **Rationale**: Clear separation of concerns, easier to understand and modify
  - **Alternatives considered**: 
    - Single file with both (less clear separation)
    - Class-based modules (adds unnecessary abstraction for simple examples)

- **Decision**: Use environment variables or hardcoded defaults for broker configuration
  - **Rationale**: Simple configuration that defaults to localhost:9092 (matching docker-compose setup)
  - **Alternatives considered**: 
    - Configuration files (adds complexity for simple use case)
    - Command-line arguments (can be added later if needed)

## Risks / Trade-offs
- **Risk**: `confluent-kafka` requires C dependencies (librdkafka)
  - **Mitigation**: Document installation requirements, provide clear setup instructions
  - **Trade-off**: More complex installation vs. better performance

- **Risk**: Port conflicts or broker not running
  - **Mitigation**: Add clear error messages, document prerequisite (docker-compose up)

- **Trade-off**: Simple examples vs. production-ready code
  - **Decision**: Prioritize simplicity and clarity for learning/experimentation

## Migration Plan
N/A - This is a new capability, no migration needed.

## Open Questions
- Should we include example scripts that demonstrate producer/consumer interaction?
- Do we want to add command-line argument support for topic names and message content?
- Should we include basic error handling examples or keep it minimal?
