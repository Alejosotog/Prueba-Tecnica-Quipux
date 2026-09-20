from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class EarthquakeQueryParams(BaseModel):
    magnitude_min: Optional[float] = Field(
        default=None,
        ge=0,
        description="Magnitud mínima"
    )

    magnitude_max: Optional[float] = Field(
        default=None,
        ge=0,
        description="Magnitud máxima"
    )

    page: int = Field(
        default=1,
        ge=1,
        description="Número de página"
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Cantidad de registros por página"
    )

    sort_by: Literal[
        "event_time",
        "magnitude",
        "location",
        "depth"
    ] = Field(
        default="event_time",
        description="Campo por el cual ordenar"
    )

    sort_order: Literal["asc", "desc"] = Field(
        default="desc",
        description="Orden de los resultados"
    )

    @model_validator(mode="after")
    def validate_magnitude_range(self):
        if (
            self.magnitude_min is not None
            and self.magnitude_max is not None
            and self.magnitude_min > self.magnitude_max
        ):
            raise ValueError(
                "magnitude_min no puede ser mayor que magnitude_max"
            )

        return self