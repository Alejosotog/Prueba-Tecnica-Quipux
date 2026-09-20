import logging
import time

from services.ingestion_service import ingest_earthquakes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


while True:
    try:
        new_events = ingest_earthquakes()
        logger.info("Eventos nuevos procesados: %s", new_events)
    except Exception:
        logger.exception("Error durante la ingesta")

    time.sleep(180)