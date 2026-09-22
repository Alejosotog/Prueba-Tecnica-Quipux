from fastapi import APIRouter

from services.metrics_service import (
    earthquakes_last_hour,
    average_magnitude_last_hour,
    max_magnitude_last_hour,
    magnitude_distribution_last_hour
)

from utils.cache import TTLCache


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


metrics_cache = TTLCache(ttl_seconds=30)


@router.get("/")
def get_metrics():

    cached_metrics = metrics_cache.get()

    if cached_metrics is not None:
        return cached_metrics

    metrics = {
        "earthquakes_last_hour": earthquakes_last_hour(),
        "average_magnitude_last_hour": average_magnitude_last_hour(),
        "max_magnitude_last_hour": max_magnitude_last_hour(),
        "magnitude_distribution": magnitude_distribution_last_hour()
    }

    metrics_cache.set(metrics)

    return metrics  