from typing import Optional
from .User import UpdateUserModel, User
from pydantic import Field


class Dispatcher(User):
    pay_per_month: float = Field(default=None, description="this field represents the dispatchers monthly pay")
    truck_driver_list: list[str | None] = Field(default=[], description="this field represents a list of truck driver ids that the dispatcher is in charge of")
    manager_id: Optional[str] = Field(default= None, description= "this field represents the id of the dispatchers manager")

class UpdateDispatcherModel(UpdateUserModel):
    pay_per_month: Optional[float] = Field(default=None, description="this field represents the dispatchers monthly pay")
    truck_driver_list: list[str | None] = Field(default=None, description="this field represents a list of truck driver ids that the dispatcher is in charge of")