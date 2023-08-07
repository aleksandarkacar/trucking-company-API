from .User import User
from typing import Optional
from pydantic import Field

class TruckDriver(User):
    pay_per_mile: float = Field(default= None, description= "this field represents how much many per mile driven the driver makes")
    current_load: Optional[str] = Field(default=None, description= "this field represents what the truck driver is currently carrying")
    dispatcher_id: str = Field(default= None, description= "this field represents the id of the truck drivers dispatcher")
    manager_id: str = Field(default= None, description= "this field represents the id of the truck drivers manager")
    truck_id: str = Field(default= None, description= "this field represents the id of the truck drivers truck")

