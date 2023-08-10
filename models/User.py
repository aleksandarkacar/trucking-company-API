from pydantic import BaseModel
from typing import Optional
from pydantic import Field

class User(BaseModel):
    id: str = Field(default=None, alias="_id", description="The unique identifier for the User")
    first_name: str = Field(default=None, description="this field represents the users frist name")
    last_name: str = Field(default=None, description="this field represents the users last name")
    birthdate: str = Field(default=None, description="this field represents the users date of birth")
    JMBG: int = Field(default=None, description="this field represents the users unique master citizen number (JMBG)")
    age: int = Field(default=None, description="this field represents the users age")
    years_of_experience: int = Field(default=None, description="this field represents how many hours of job experience the user has")
    working_area: Optional[str] = Field(default=None, description="this field represents what area the user is working in")
    working_hours_month: int = Field(default=None, description="this field represents how many hours a month the user works")
    
class UpdateUserModel(BaseModel):
    working_area: Optional[str] = Field(default=None, description="this field represents what area the user is working in")


