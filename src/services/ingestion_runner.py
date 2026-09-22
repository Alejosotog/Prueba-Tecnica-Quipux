import json
import logging
import time
from datetime import datetime, timezone

from prometheus_client import start_http_server

from services.ingestion_service import ingest_earthquakes


class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "event"):
            log_data["event"] = record.event

        if hasattr(record, "received"):
            log_data["received"] = record.received

        if hasattr(record, "new"):
            log_data["new"] = record.new

        if hasattr(record, "existing"):
            log_data["existing"] = record.existing

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

for handler in logging.getLogger().handlers:
    handler.setFormatter(StructuredFormatter())


logger = logging.getLogger(__name__)


# Endpoint Prometheus del proceso de ingesta
start_http_server(8001)


while True:
    try:
        new_events = ingest_earthquakes()

        logger.info(
            "Ingesta completada",
            extra={
                "event": "ingestion_completed",
                "new": new_events,
            },
        )

    except Exception:
        logger.exception(
            "Error durante la ingesta",
            extra={
                "event": "ingestion_error",
            },
        )

    time.sleep(180)