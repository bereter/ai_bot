from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Chat
from .shemas import ChatCreate
from sqlalchemy.orm import joinedload, join
from typing import Sequence


async def get_chat(session: AsyncSession, id_chat: int) -> Chat | None:
    return await session.get(Chat, id_chat)


# async def get_chats(session: AsyncSession) -> list[Chat] | None:
#     stmt = select(Chat).order_by(Chat.id)
#     result: Result = await session.execute(stmt)
#     chats = result.scalars().all()
#     return list(chats)


async def create_chat(session: AsyncSession, chat_in: ChatCreate) -> Chat:
    chat = Chat(**chat_in.model_dump())
    session.add(chat)
    await session.commit()
    return chat

