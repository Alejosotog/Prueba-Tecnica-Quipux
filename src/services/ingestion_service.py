import logging
import time
from messaging.rabbitmq_producer import publish_earthquake  

from clients.usgs_client import get_earthquakes
from database.earthquake_repository import save_earthquake
from database.connection import earthquakes_collection
from services.metrics_service import save_current_metrics
from utils.transformers import transform_earthquake
from utils.prometheus_metrics import (
    ingestion_events_received,
    ingestion_events_new,
    ingestion_errors,
    ingestion_duration,
    stored_earthquakes,
)

logger = logging.getLogger(__name__)


def ingest_earthquakes():
    start_time = time.perf_counter()

    try:
        data = get_earthquakes()

        features = data.get("features", [])
        total_events = len(features)

        ingestion_events_received.inc(total_events)

        new_events = 0

        for feature in features:
            earthquake = transform_earthquake(feature)
            is_new = save_earthquake(earthquake)

            if is_new:
                new_events += 1
                ingestion_events_new.inc()
                publish_earthquake(earthquake)

        save_current_metrics()

        stored_count = earthquakes_collection.count_documents({})
        stored_earthquakes.set(stored_count)

        logger.info(
            "Ingesta completada: recibidos=%s, nuevos=%s, existentes=%s",
            total_events,
            new_events,
            total_events - new_events,
        )

        logger.info("Métricas actualizadas después de la ingesta.")

        return new_events

    except Exception:
        ingestion_errors.inc()
        raise

    finally:
        duration = time.perf_counter() - start_time
        ingestion_duration.observe(duration)