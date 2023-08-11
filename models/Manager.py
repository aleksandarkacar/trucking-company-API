from typing import Optional
from .User import UpdateUserModel, User
from pydantic import Field

class Manager(User):
    pay_per_month: float = Field(default=None, description="this field represents the managers monthly pay")
    truck_driver_list: list[str | None] = Field(default=[], description="this field represents a list of truck driver ids that the manager is in charge of")
    dispatcher_list: list[str | None] = Field(default=[], description="this field represents a list of dispatcher ids that the manager is in charge of")

class UpdateManagerModel(UpdateUserModel):
    pay_per_month: Optional[float] = Field(default=None, description="this field represents the managers monthly pay")
    truck_driver_list: list[str | None] = Field(default=None, description="this field represents a list of truck driver ids that the manager is in charge of")
    dispatcher_list: list[str | None] = Field(default=None, description="this field represents a list of dispatcher ids that the manager is in charge of")