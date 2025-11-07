# alx_travel_app
ALX travel app


## Running RabbitMQ + Celery (local development)

### Start RabbitMQ (docker-compose)
Create a `docker-compose.yml` (or use the snippet below) and run `docker-compose up -d`:

```yaml
version: "3"
services:
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
