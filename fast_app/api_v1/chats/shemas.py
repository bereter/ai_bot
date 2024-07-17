from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatBase(BaseModel):
    message_user: str
    user_id: int


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    model_config = ConfigDict(from_attributes=True)
    message_ai: str
    id: int
    datetime: datetime


