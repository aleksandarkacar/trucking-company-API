from pydantic import BaseModel
from typing import Optional
from pydantic import Field
from .Repair import RepairModel

class Vehicle(BaseModel):
    wheels: int = Field(default=None, description="This field represents how many wheels the vehicle has")
    miles: int = Field(default=None, description="This field represents how many miles the vehicle has traveled")
    manufacturing_year: str = Field(default=None, description="This field represents what year the vehicle was manufactured")
    repair_history_list: list[RepairModel|None] = Field(default=None, description="This feild holds a list of all repairs the vegicle has undergone")

class UpdateVehicleModel(BaseModel):
    miles: Optional[int] = Field(default= None, description="This field represents the new miles traveled for the truck")
    repair_history_list: Optional[list[RepairModel | None]] = Field(default= None, description="This field represents the new repair list of truck")