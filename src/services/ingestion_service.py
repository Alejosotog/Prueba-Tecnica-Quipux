import logging

from clients.usgs_client import get_earthquakes
from database.earthquake_repository import save_earthquake
from services.metrics_service import save_current_metrics
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

    # Actualizar y persistir las métricas
    # después de procesar los eventos recibidos.
    save_current_metrics()

    logger.info(
        "Ingesta completada: recibidos=%s, nuevos=%s, existentes=%s",
        total_events,
        new_events,
        total_events - new_events,
    )

    logger.info(
        "Métricas actualizadas después de la ingesta."
    )

    return new_events