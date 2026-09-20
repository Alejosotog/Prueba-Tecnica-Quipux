from typing import Optional

from fastapi import APIRouter, Query, HTTPException

from database.connection import earthquakes_collection


router = APIRouter(
    prefix="/earthquakes",
    tags=["Earthquakes"]
)


@router.get("/")
def get_earthquakes(
    magnitude_min: Optional[float] = Query(
        None,
        ge=0,
        description="Magnitud mínima"
    ),
    magnitude_max: Optional[float] = Query(
        None,
        ge=0,
        description="Magnitud máxima"
    ),
    page: int = Query(
        1,
        ge=1,
        description="Número de página"
    ),
    page_size: int = Query(
        20,
        ge=1,
        le=100,
        description="Cantidad de registros por página"
    ),
    sort_by: str = Query(
        "event_time",
        description="Campo por el cual ordenar"
    ),
    sort_order: str = Query(
        "desc",
        pattern="^(asc|desc)$",
        description="Orden ascendente o descendente"
    )
):
    """
    Consulta eventos sísmicos almacenados en MongoDB.
    """

    if (
        magnitude_min is not None
        and magnitude_max is not None
        and magnitude_min > magnitude_max
    ):
        raise HTTPException(
            status_code=400,
            detail="magnitude_min no puede ser mayor que magnitude_max"
        )

    query = {}

    # Filtro por magnitud mínima
    if magnitude_min is not None:
        query.setdefault("magnitude", {})["$gte"] = magnitude_min

    # Filtro por magnitud máxima
    if magnitude_max is not None:
        query.setdefault("magnitude", {})["$lte"] = magnitude_max

    # Campos permitidos para ordenar
    allowed_sort_fields = {
        "event_time",
        "magnitude",
        "location",
        "depth"
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"sort_by debe ser uno de: {', '.join(allowed_sort_fields)}"
        )

    sort_direction = 1 if sort_order == "asc" else -1

    skip = (page - 1) * page_size

    total = earthquakes_collection.count_documents(query)

    cursor = (
        earthquakes_collection
        .find(query)
        .sort(sort_by, sort_direction)
        .skip(skip)
        .limit(page_size)
    )

    earthquakes = list(cursor)

    for earthquake in earthquakes:
        earthquake["_id"] = str(earthquake["_id"])

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
        "data": earthquakes
    }