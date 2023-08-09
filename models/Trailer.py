from .Vehicle import UpdateVehicleModel, Vehicle
from typing import Optional
from pydantic import Field


class Trailer(Vehicle):
    truck_id: Optional[str] = Field(default=None, description="this feld represents the id of the truck it is connected to")

class UpdateTrailerModel(UpdateVehicleModel):
    # truck_id: Optional[str] = Field(default= None, descripton = "this field represents the id of the truck conected to this trailer if there is one")
    pass
