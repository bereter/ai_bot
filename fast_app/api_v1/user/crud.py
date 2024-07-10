from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from .shemas import UserCreate


async def get_user(session: AsyncSession, id_user: int) -> User | None:
    return await session.get(User, id_user)


async def get_user_by_email(session: AsyncSession, user_email: str, password: str) -> User | None:
    stmt = select(User).filter_by(user_email=user_email, password=password)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    return user
    # return await session.query(User).filter(User.user_email == user_email, User.password == password).first()


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user




