# Local Kafka

## Purpose
Docker Compose-based local Kafka broker for development and testing.

## Requirements

### Requirement: Local Kafka Infrastructure
The project SHALL provide a Docker Compose configuration that enables running a Kafka broker locally for development and testing purposes.

#### Scenario: Start local Kafka environment
- **WHEN** a developer runs `docker-compose up`
- **THEN** Zookeeper and Kafka broker services start successfully
- **AND** Kafka broker is accessible on port 9092 from the host machine
- **AND** services are healthy and ready to accept connections

#### Scenario: Stop local Kafka environment
- **WHEN** a developer runs `docker-compose down`
- **THEN** all Kafka-related services stop gracefully
- **AND** containers are removed

#### Scenario: Connect to local Kafka broker
- **WHEN** a Kafka client application connects to `localhost:9092`
- **THEN** the connection is established successfully
- **AND** the client can produce and consume messages

#### Scenario: Persist Kafka data across restarts
- **WHEN** Docker Compose services are stopped and restarted
- **THEN** previously created topics and messages are preserved
- **AND** data persists in Docker volumes
