from .Vehicle import Vehicle
from typing import Optional
from pydantic import Field


class Trailer(Vehicle):
    truck_id: Optional[str] = Field(default=None, description="this feld represents the id of the truck it is connected to")
