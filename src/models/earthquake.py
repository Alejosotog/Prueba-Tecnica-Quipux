from datetime import datetime
from pydantic import BaseModel


class Earthquake(BaseModel):
    event_id: str
    magnitude: float
    location: str
    latitude: float
    longitude: float
    depth: float
    event_time: datetime
    magnitude_range: str