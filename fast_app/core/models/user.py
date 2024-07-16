from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import DateTime, TIMESTAMP
from datetime import datetime

if TYPE_CHECKING:
    from .chat import Chat


class User(Base):
    __tablename__ = 'user'

    username: Mapped[str]
    password: Mapped[str]
    user_email: Mapped[str] = mapped_column(unique=True)
    datetime: Mapped[DateTime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    chats: Mapped[list['Chat']] = relationship(back_populates='user')


    def __repr__(self):
        return f'User: {self.username}, id: {self.id}'
