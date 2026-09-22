import json
import os
import pika


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "quipux")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "quipux123")

EXCHANGE_NAME = "earthquake.events"


def publish_earthquake(earthquake):
    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials
        )
    )

    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="fanout",
        durable=True
    )

    message = json.dumps(
        earthquake,
        default=str,
        ensure_ascii=False
    )

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key="",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json"
        )
    )

    connection.close()