## Context
This change introduces Docker Compose configuration to run Apache Kafka locally for development and testing purposes. The setup needs to be simple, reliable, and accessible from the host machine.

## Goals / Non-Goals
- **Goals**:
  - Provide a single-command way to start Kafka broker locally
  - Make Kafka accessible from host applications (not just containers)
  - Use official Kafka Docker images for reliability
  - Support basic Kafka operations (produce/consume messages)
  
- **Non-Goals**:
  - Multi-broker cluster setup (single broker is sufficient for local dev)
  - Schema Registry integration (can be added later if needed)
  - Kafka UI tools (can be added separately if desired)
  - Production-ready configuration (this is for local development only)

## Decisions
- **Decision**: Use Confluent Platform Docker images
  - **Rationale**: Well-maintained, official images with good documentation
  - **Alternatives considered**: 
    - Apache Kafka official images (also viable, but Confluent images are more commonly used)
    - Bitnami Kafka images (good alternative, but Confluent is more standard)

- **Decision**: Expose Kafka on port 9092 (standard port)
  - **Rationale**: Standard Kafka port, matches default client configurations
  - **Alternatives considered**: Custom port (adds unnecessary configuration complexity)

- **Decision**: Include Zookeeper (required for Kafka < 2.8, or use KRaft mode for newer versions)
  - **Rationale**: Zookeeper is still the most common setup and works with all Kafka versions
  - **Alternatives considered**: KRaft mode (Kafka without Zookeeper) - can be added as alternative later

- **Decision**: Use environment variables for configuration
  - **Rationale**: Easy to customize without modifying docker-compose.yml
  - **Alternatives considered**: Hardcoded values (less flexible)

## Risks / Trade-offs
- **Risk**: Port conflicts if 9092 or 2181 already in use
  - **Mitigation**: Document port requirements, allow port customization via environment variables

- **Risk**: Data persistence across restarts
  - **Mitigation**: Use Docker volumes for Kafka and Zookeeper data directories

- **Trade-off**: Single broker vs. multi-broker cluster
  - **Decision**: Single broker for simplicity (sufficient for local development)

## Migration Plan
N/A - This is a new capability, no migration needed.

## Open Questions
- Should we include Kafka UI (like kafka-ui or kafdrop) in the initial setup?
- Do we want to pre-create any topics on startup?
- Should we configure log retention policies for local development?
