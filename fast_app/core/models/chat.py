from typing import TYPE_CHECKING

from .base import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, TIMESTAMP, ForeignKey, String

if TYPE_CHECKING:
    from .user import User


class Chat(Base):
    __tablename__ = 'chat'

    message: Mapped[str]
    datetime: Mapped[DateTime] = mapped_column(TIMESTAMP, default=datetime.now())
    themes: Mapped[str] = mapped_column(String(2))
    path_to_audio: Mapped[str | None]
    message_from: Mapped[str] = mapped_column(String(2))

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='chats')

    def __repr__(self):
        return f'Chat id: {self.id}, User: {self.user_id}'
