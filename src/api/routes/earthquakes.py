from typing import Annotated

from fastapi import APIRouter, Query

from database.connection import earthquakes_collection
from models.earthquake_query import EarthquakeQueryParams


router = APIRouter(
    prefix="/earthquakes",
    tags=["Earthquakes"]
)


@router.get("/")
def get_earthquakes(
    params: Annotated[EarthquakeQueryParams, Query()]
):
    query = {}

    if params.magnitude_min is not None:
        query.setdefault("magnitude", {})["$gte"] = params.magnitude_min

    if params.magnitude_max is not None:
        query.setdefault("magnitude", {})["$lte"] = params.magnitude_max

    sort_direction = 1 if params.sort_order == "asc" else -1

    skip = (params.page - 1) * params.page_size

    total = earthquakes_collection.count_documents(query)

    cursor = (
        earthquakes_collection
        .find(query)
        .sort(params.sort_by, sort_direction)
        .skip(skip)
        .limit(params.page_size)
    )

    earthquakes = list(cursor)

    for earthquake in earthquakes:
        earthquake["_id"] = str(earthquake["_id"])

    return {
        "page": params.page,
        "page_size": params.page_size,
        "total": total,
        "total_pages": (
            (total + params.page_size - 1)
            // params.page_size
        ),
        "data": earthquakes
    }