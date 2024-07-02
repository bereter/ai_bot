from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatBase(BaseModel):
    message_user: str
    message_ai: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    datetime: datetime

