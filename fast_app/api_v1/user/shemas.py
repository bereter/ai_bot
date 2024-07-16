from typing import Annotated
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from api_v1.chats.shemas import Chat


class UserBase(BaseModel):
    username: str
    user_email: EmailStr


class UserCreate(UserBase):
    password: str


class UserList(UserBase):
    id: int
    datetime: datetime
    chats: list[Chat] = []


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    datetime: datetime

