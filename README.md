# Kafka Test Project

A testing and experimentation project for Apache Kafka.

## Prerequisites

- Docker
- Docker Compose
- Python 3.8 or higher (for Python Kafka clients)

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

## Python Kafka Clients

This project includes Python producer and consumer clients for interacting with the local Kafka broker.

### Setup

1. **Create and activate a virtual environment:**
   
   A virtual environment isolates Python dependencies for this project. Create one as follows:
   
   ```bash
   # Create virtual environment (creates a 'venv' directory)
   python3 -m venv venv
   ```
   
   **Activate the virtual environment:**
   
   - **On Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
   
   - **On Windows (Command Prompt):**
     ```bash
     venv\Scripts\activate
     ```
   
   - **On Windows (PowerShell):**
     ```bash
     venv\Scripts\Activate.ps1
     ```
   
   **Verify activation:** When activated, you should see `(venv)` at the beginning of your command prompt:
   ```bash
   (venv) user@hostname:~/kafka-test$
   ```
   
   **Note:** You'll need to activate the virtual environment each time you open a new terminal session. To deactivate it later, simply run:
   ```bash
   deactivate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Note: The `confluent-kafka` library requires C dependencies (librdkafka). On some systems, you may need to install system packages first:
   - **Ubuntu/Debian**: `sudo apt-get install librdkafka-dev`
   - **macOS**: `brew install librdkafka`
   - **Windows**: Pre-built wheels are usually available via pip

3. **Ensure Kafka broker is running:**
   ```bash
   docker-compose up -d
   ```

### Usage

#### Producer

Send messages to a Kafka topic:

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows

python producer.py
```

The producer will:
- Connect to `localhost:9092` (or `KAFKA_BOOTSTRAP_SERVERS` environment variable)
- Send a JSON message to the `test-topic` (or `KAFKA_TOPIC` environment variable)

**Example:**
```python
from producer import create_producer, produce_message

producer = create_producer()
message = {'key': 'value', 'timestamp': '2024-01-01T00:00:00Z'}
produce_message(producer, 'my-topic', message)
```

#### Consumer

Read messages from a Kafka topic:

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows

python consumer.py
```

The consumer will:
- Connect to `localhost:9092` (or `KAFKA_BOOTSTRAP_SERVERS` environment variable)
- Subscribe to the `test-topic` (or `KAFKA_TOPIC` environment variable)
- Use consumer group `python-consumer-group` (or `KAFKA_CONSUMER_GROUP` environment variable)
- Consume up to 10 messages and exit

**Example:**
```python
from consumer import create_consumer, consume_messages

consumer = create_consumer()
for topic, partition, offset, message in consume_messages(consumer, 'my-topic'):
    print(f"Received: {message}")
```

### Environment Variables

You can customize the Kafka connection using environment variables:

- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker address (default: `localhost:9092`)
- `KAFKA_TOPIC`: Default topic name (default: `test-topic`)
- `KAFKA_CONSUMER_GROUP`: Consumer group ID (default: `python-consumer-group`)

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
├── producer.py           # Python Kafka producer client
├── consumer.py           # Python Kafka consumer client
├── requirements.txt      # Python dependencies
└── openspec/             # OpenSpec specifications
```

## Development

This project uses OpenSpec for spec-driven development. See `openspec/AGENTS.md` for workflow details.
