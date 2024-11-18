from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatBase(BaseModel):
    message_user: str
    user_id: int


class ChatCreate(ChatBase):
    pass


class Chat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    message: str
    themes: str
    path_to_audio: str | None
    message_from: str
    datetime: datetime


