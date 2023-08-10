from pydantic import BaseModel
from pydantic import Field

class RepairModel(BaseModel):
    id: str = Field(default=None, alias="_id", description="The unique identifier for the Repair")
    date: str = Field(default=None, description="this field represents what date this repair took place")
    type: str = Field(defailt=None, description="this field represents what type of repair was performed")


    