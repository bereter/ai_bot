from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Chat
from .shemas import ChatCreate

from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


async def message_ai(message_user: str) -> str:
    # Авторизация в сервисе GigaChat
    chat_ai = GigaChat(
        credentials=getenv('KEY_GIGA_CHAT'),
        verify_ssl_certs=False)

    # Добавление системного сообщения с указанием роли "Генри Форда" и запросом истории
    messages = [
        SystemMessage(
            content="Ты Генри Форд. Отвечай как он, рассказывай свою историю.",
            role="Генри Форд"
        ),
        HumanMessage(content=message_user)
    ]

    res = chat_ai(messages)
    return res.content


async def get_chat(session: AsyncSession, id_chat: int) -> Chat | None:
    return await session.get(Chat, id_chat)


async def create_chat(session: AsyncSession, chat_in: ChatCreate) -> Chat:
    res_ai = await message_ai(chat_in.message_user)
    chat = Chat(**chat_in.model_dump(), message_ai=res_ai)
    session.add(chat)
    await session.commit()
    return chat


