from datetime import datetime, timedelta, timezone

from database.connection import earthquakes_collection
from database.metrics_repository import save_metrics


def time_range_last_hour():
    now = datetime.now(timezone.utc)
    one_hour_ago = now - timedelta(hours=1)

    return one_hour_ago, now


def earthquakes_last_hour():
    one_hour_ago, now = time_range_last_hour()

    return earthquakes_collection.count_documents(
        {
            "event_time": {
                "$gte": one_hour_ago,
                "$lte": now
            }
        }
    )


def average_magnitude_last_hour():
    one_hour_ago, now = time_range_last_hour()

    result = list(
        earthquakes_collection.aggregate(
            [
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
                        "_id": None,
                        "average_magnitude": {"$avg": "$magnitude"}
                    }
                }
            ]
        )
    )

    if not result:
        return 0

    return result[0]["average_magnitude"]


def max_magnitude_last_hour():
    one_hour_ago, now = time_range_last_hour()

    result = list(
        earthquakes_collection.aggregate(
            [
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
                        "_id": None,
                        "max_magnitude": {"$max": "$magnitude"}
                    }
                }
            ]
        )
    )

    if not result:
        return 0

    return result[0]["max_magnitude"]


def magnitude_distribution_last_hour():
    one_hour_ago, now = time_range_last_hour()

    distribution = {
        "Micro": 0,
        "Menor": 0,
        "Ligero": 0,
        "Moderado": 0,
        "Fuerte": 0
    }

    result = earthquakes_collection.aggregate(
        [
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
                    "_id": "$magnitude_range",
                    "count": {"$sum": 1}
                }
            }
        ]
    )

    for item in result:
        if item["_id"] in distribution:
            distribution[item["_id"]] = item["count"]

    return distribution


def magnitude_range(magnitude):
    if magnitude < 2.0:
        return "Micro"
    elif magnitude < 4.0:
        return "Menor"
    elif magnitude < 5.0:
        return "Ligero"
    elif magnitude < 6.0:
        return "Moderado"
    else:
        return "Fuerte"


def save_current_metrics():
    metrics = {
        "calculated_at": datetime.now(timezone.utc),
        "earthquakes_last_hour": earthquakes_last_hour(),
        "average_magnitude_last_hour": average_magnitude_last_hour(),
        "max_magnitude_last_hour": max_magnitude_last_hour(),
        "magnitude_distribution": magnitude_distribution_last_hour()
    }

    save_metrics(metrics)
