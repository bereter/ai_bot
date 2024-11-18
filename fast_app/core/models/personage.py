from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Personage(Base):
    __tablename__ = 'personage'

    status: Mapped[str]
    themes: Mapped[str] = mapped_column(String(2))

    def __repr__(self):
        return f'{self.themes}: {self.status[0:30]}'
