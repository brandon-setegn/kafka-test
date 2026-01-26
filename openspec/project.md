# Project Context

## Purpose
A testing and experimentation project for Apache Kafka. This project is used to:
- Test Kafka producer and consumer functionality
- Experiment with different Kafka configurations and patterns
- Learn and validate Kafka concepts and best practices
- Develop reusable Kafka utilities and examples

## Tech Stack
- **Apache Kafka** - Distributed event streaming platform
- **Language**: To be determined (common options: Java, Python, Node.js, Go)
- **Build Tool**: To be determined (Maven/Gradle for Java, pip/poetry for Python, npm/yarn for Node.js)
- **Testing Framework**: To be determined based on language choice

## Project Conventions

### Code Style
- Use clear, descriptive variable and function names
- Follow language-specific style guides (PEP 8 for Python, Google Java Style for Java, etc.)
- Keep functions focused and single-purpose
- Add comments for complex logic or Kafka-specific configurations

### Architecture Patterns
- Separate producer and consumer logic into distinct modules/components
- Use configuration files for Kafka connection settings (brokers, topics, etc.)
- Implement error handling and retry logic for Kafka operations
- Follow Kafka best practices for partitioning, serialization, and consumer groups

### Testing Strategy
- Write unit tests for business logic
- Include integration tests for Kafka producer/consumer interactions
- Use test containers or embedded Kafka for local testing when possible
- Test error scenarios and edge cases (connection failures, message serialization errors, etc.)

### Git Workflow
- Use feature branches for new functionality (`feature/kafka-producer`, `feature/kafka-consumer`)
- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Use conventional commit format when possible (e.g., `feat: add Kafka producer`, `test: add consumer integration tests`)

## Domain Context
- **Kafka Topics**: Named channels for organizing messages
- **Producers**: Applications that publish messages to topics
- **Consumers**: Applications that read messages from topics
- **Consumer Groups**: Groups of consumers that work together to consume messages
- **Partitions**: Topics are divided into partitions for parallelism and scalability
- **Brokers**: Kafka servers that store and serve messages

## Important Constraints
- Kafka broker must be accessible (local or remote)
- Consider message serialization format (JSON, Avro, Protobuf, etc.)
- Handle Kafka connection failures gracefully
- Consider message ordering requirements when using multiple partitions

## External Dependencies
- **Apache Kafka** - Requires Kafka broker(s) to be running
- **Kafka Client Libraries** - Language-specific Kafka client libraries
- **Optional**: Schema Registry (if using Avro or other schema-based serialization)
