from datetime import datetime, timezone

from models.earthquake import Earthquake
from services.metrics_service import magnitude_range


def transform_earthquake(feature) -> Earthquake:
    properties = feature["properties"]
    coordinates = feature["geometry"]["coordinates"]

    event_time = datetime.fromtimestamp(
        properties["time"] / 1000,
        tz=timezone.utc
    )

    range_name = magnitude_range(properties["mag"])

    return Earthquake(
        event_id=feature["id"],
        magnitude=properties["mag"],
        location=properties["place"],
        longitude=coordinates[0],
        latitude=coordinates[1],
        depth=coordinates[2],
        event_time=event_time,
        magnitude_range=range_name
    )