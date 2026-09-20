from datetime import datetime, timezone

from database.connection import earthquakes_collection
from database.reports_repository import save_report
from services.metrics_service import (
    earthquakes_last_hour,
    average_magnitude_last_hour,
    max_magnitude_last_hour,
    magnitude_distribution_last_hour,
    time_range_last_hour,
)


def get_top_locations(limit=5):
    one_hour_ago, now = time_range_last_hour()

    result = earthquakes_collection.aggregate([
        {
            "$match": {
                "event_time": {
                    "$gte": one_hour_ago,
                    "$lte": now
                }
            }
        },
        {
            "$group": {
                "_id": "$location",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
            "$limit": limit
        }
    ])

    return [
        {
            "location": item["_id"],
            "count": item["count"]
        }
        for item in result
    ]


def generate_hourly_report():
    now = datetime.now(timezone.utc)

    report = {
        "report_date": now,
        "generated_at": now,
        "total_events": earthquakes_last_hour(),
        "average_magnitude": average_magnitude_last_hour(),
        "max_magnitude": max_magnitude_last_hour(),
        "top_locations": get_top_locations(),
        "magnitude_distribution": magnitude_distribution_last_hour()
    }

    save_report(report)

    return report