from pydantic import BaseModel
from pydantic import Field

class RepairModel(BaseModel):
    date: str = Field(default=None, description="this field represents what date this repair took place")
    type: str = Field(defailt=None, description="this field represents what type of repair was performed")