# Kafka Test Project

A testing and experimentation project for Apache Kafka.

## Prerequisites

- Docker
- Docker Compose

## Local Kafka Setup

This project includes a Docker Compose configuration to run Kafka locally for development and testing.

### Starting Kafka

To start the local Kafka broker and Zookeeper:

```bash
docker-compose up -d
```

This will start:
- **Zookeeper** on port `2181` (default)
- **Kafka broker** on port `9092` (default)

### Stopping Kafka

To stop the services:

```bash
docker-compose down
```

To stop and remove volumes (clears all data):

```bash
docker-compose down -v
```

### Connecting to Kafka

Once started, Kafka is accessible at:
- **Broker**: `localhost:9092`

You can use any Kafka client library to connect to this broker.

### Customizing Ports

If you need to use different ports, create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` to set your preferred ports:
```
ZOOKEEPER_PORT=2181
KAFKA_PORT=9092
```

### Data Persistence

Kafka and Zookeeper data are persisted in Docker volumes. This means:
- Topics and messages persist across container restarts
- Data is preserved when you run `docker-compose down`
- To clear all data, use `docker-compose down -v`

### Health Checks

Both services include health checks:
- Zookeeper: Checks port 2181
- Kafka: Verifies broker API is accessible

You can check service status with:
```bash
docker-compose ps
```

## Project Structure

```
.
├── docker-compose.yml    # Local Kafka infrastructure
├── .env.example          # Environment variable template
└── openspec/             # OpenSpec specifications
```

## Development

This project uses OpenSpec for spec-driven development. See `openspec/AGENTS.md` for workflow details.
