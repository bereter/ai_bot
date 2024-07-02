from .base import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, TIMESTAMP
from sqlalchemy.sql import func


class Chat(Base):
    __tablename__ = 'chats'

    message_user: Mapped[str]
    message_ai: Mapped[str]
    datetime: Mapped[DateTime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
