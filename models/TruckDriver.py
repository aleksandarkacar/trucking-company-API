from .User import UpdateUserModel, User
from typing import Optional
from pydantic import Field

class TruckDriver(User):
    pay_per_mile: float = Field(default= None, description= "this field represents how much many per mile driven the driver makes")
    current_load: Optional[str] = Field(default=None, description= "this field represents what the truck driver is currently carrying")
    dispatcher_id: Optional[str] = Field(default= None, description= "this field represents the id of the truck drivers dispatcher")
    manager_id: Optional[str] = Field(default= None, description= "this field represents the id of the truck drivers manager")
    truck_id: Optional[str] = Field(default= None, description= "this field represents the id of the truck drivers truck")

class UpdateTruckDriverModel(UpdateUserModel):
    truck_id: Optional[str] = Field(default= None, description= "this field represents the id of the truck drivers truck")
    current_load: Optional[str] = Field(default=None, description= "this field represents what the truck driver is currently carrying")


