from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Chat
from .shemas import ChatCreate

async def get_chats(session: AsyncSession) -> list[Chat]:
    stmt = select(Chat).order_by(Chat.id)
    result: Result = await session.execute(stmt)
    chats = result.scalars().all()
    return list(chats)


async def create_chats(session: AsyncSession, chat_in: ChatCreate) -> Chat:
    chat = Chat(**chat_in.model_dump())
    session.add(chat)
    await session.commit()
    # await session.refresh(chat)
    return chat

