from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User, Chat
from .shemas import UserCreate
from sqlalchemy.orm import selectinload, contains_eager


async def get_user(session: AsyncSession, id_user: int) -> User | None:
    return await session.get(User, id_user)


async def get_user_by_email(session: AsyncSession, user_email: str, password: str) -> User | None:
    stmt = select(User).filter_by(user_email=user_email, password=password)
    result: Result = await session.execute(stmt)
    user = result.scalars().one()
    return user


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_user_chats(session: AsyncSession, id_user: int, limit: int, offset: int) -> User | None:
    subq = (
        select(Chat.id)
        .filter(Chat.user_id == User.id)
        .order_by(Chat.datetime.desc())
        .limit(limit)
        .offset(offset)
        .scalar_subquery()
        .correlate(User)
    )
    stmt = (
        select(User)
        .filter_by(id=id_user)
        .outerjoin(Chat, Chat.id.in_(subq))
        .options(contains_eager(User.chats))
        )
    result: Result = await session.execute(stmt)
    user_chats = result.unique().scalars().one_or_none()
    return user_chats




