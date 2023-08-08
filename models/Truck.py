from typing import Optional
from .Vehicle import Vehicle, UpdateVehicleModel
from pydantic import Field, BaseModel

class Truck(Vehicle):
    horsepower: int = Field(default= None, description= "this field represents how much horse power the truck has")
    driver_id: Optional[str] = Field(default= None, descripton = "this field represents the id of driver of the truck if one is assigned")
    trailer_id: Optional[str] = Field(default= None, descripton = "this field represents the id of the trailer conected to truck if there is one")

class UpdateTruckmodel(UpdateVehicleModel):
    horsepower: Optional[int] = Field(default= None, description= "this field represents how much horse power the truck has")
    driver_id: Optional[str] = Field(default= None, descripton = "this field represents the id of driver of the truck if one is assigned")
    trailer_id: Optional[str] = Field(default= None, descripton = "this field represents the id of the trailer conected to truck if there is one")