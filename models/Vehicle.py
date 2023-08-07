from pydantic import BaseModel
from pydantic import Field
from .Repair import Repair

class Vehicle(BaseModel):
    wheels: int = Field(default=None, description="This field represents how many wheels the vehicle has")
    miles: int = Field(default=None, description="This field represents how many miles the vehicle has traveled")
    manufacturing_year: str = Field(default=None, description="This field represents what year the vehicle was manufactured")
    repair_history_list: list[Repair|None] = Field(default=None, description="This feild holds a list of all repairs the vegicle has undergone")