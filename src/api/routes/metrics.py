from fastapi import APIRouter

from services.metrics_service import (
    earthquakes_last_hour,
    average_magnitude_last_hour,
    max_magnitude_last_hour,
    magnitude_distribution_last_hour
)


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


@router.get("/")
def get_metrics():
    return {
        "earthquakes_last_hour": earthquakes_last_hour(),
        "average_magnitude_last_hour": average_magnitude_last_hour(),
        "max_magnitude_last_hour": max_magnitude_last_hour(),
        "magnitude_distribution": magnitude_distribution_last_hour()
    }
