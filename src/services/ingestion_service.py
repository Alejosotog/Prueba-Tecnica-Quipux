import logging

from clients.usgs_client import get_earthquakes
from database.earthquake_repository import save_earthquake
from utils.transformers import transform_earthquake

logger = logging.getLogger(__name__)


def ingest_earthquakes():
    data = get_earthquakes()

    total_events = len(data.get("features", []))
    new_events = 0

    for feature in data.get("features", []):
        earthquake = transform_earthquake(feature)
        is_new = save_earthquake(earthquake)

        if is_new:
            new_events += 1

    logger.info(
        "Ingesta completada: recibidos=%s, nuevos=%s, existentes=%s",
        total_events,
        new_events,
        total_events - new_events,
    )

    return new_events