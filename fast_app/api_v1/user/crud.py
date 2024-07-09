from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from .shemas import UserCreate


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def get_user(session: AsyncSession, id_user: int) -> User | None:
    return await session.get(User, id_user)

