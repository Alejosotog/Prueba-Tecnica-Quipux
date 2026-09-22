import json
import logging
import os
import time

import pika


logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "quipux")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "quipux123")

EXCHANGE_NAME = "earthquake.events"
QUEUE_NAME = "earthquake_events"


def process_earthquake(message):
    """Procesa un evento sísmico recibido desde RabbitMQ."""

    if isinstance(message, bytes):
        message = message.decode("utf-8")

    if isinstance(message, str):
        earthquake = json.loads(message)
    else:
        earthquake = message

    logger.info(
        "Evento sísmico procesado desde RabbitMQ",
        extra={
            "event": "earthquake_processed",
            "event_id": earthquake.get("event_id"),
            "magnitude": earthquake.get("magnitude"),
            "location": earthquake.get("location"),
        },
    )


def callback(channel, method, properties, body):
    try:
        process_earthquake(body)

        channel.basic_ack(
            delivery_tag=method.delivery_tag
        )

    except Exception:
        logger.exception(
            "Error procesando evento desde RabbitMQ",
            extra={
                "event": "rabbitmq_processing_error"
            },
        )

        channel.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )


def start_consumer():
    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD
    )

    while True:
        connection = None

        try:
            logger.info(
                "Intentando conectar con RabbitMQ",
                extra={
                    "event": "rabbitmq_connection_attempt"
                },
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

            channel.queue_declare(
                queue=QUEUE_NAME,
                durable=True
            )

            channel.queue_bind(
                exchange=EXCHANGE_NAME,
                queue=QUEUE_NAME
            )

            channel.basic_qos(
                prefetch_count=1
            )

            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback
            )

            logger.info(
                "Consumidor RabbitMQ iniciado",
                extra={
                    "event": "rabbitmq_consumer_started"
                },
            )

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            logger.warning(
                "RabbitMQ todavía no está disponible. "
                "Reintentando en 5 segundos.",
                extra={
                    "event": "rabbitmq_connection_retry"
                },
            )

            time.sleep(5)

        except Exception:
            logger.exception(
                "Error inesperado en el consumidor RabbitMQ",
                extra={
                    "event": "rabbitmq_consumer_error"
                },
            )

            time.sleep(5)

        finally:
            if connection is not None and not connection.is_closed:
                connection.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO
    )

    start_consumer()