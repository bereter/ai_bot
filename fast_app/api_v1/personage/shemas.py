from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class Personage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str
    themes: str