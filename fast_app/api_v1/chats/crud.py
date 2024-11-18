from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Chat

from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

import pathlib
from os import getenv
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv())


# тестовая функция
async def message_ai(message_user: str) -> str:
    # Авторизация в сервисе GigaChat
    chat_ai = GigaChat(
        credentials=getenv('KEY_GIGA_CHAT'),
        verify_ssl_certs=False
    )

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


# получение чата по id
async def get_chat(session: AsyncSession, id_chat: int) -> Chat | None:
    return await session.get(Chat, id_chat)


# создание сообщения
async def create_chat(session: AsyncSession, user_id: int, message_user: str, themes: str, audio) -> Chat:
    if audio:
        file_path = pathlib.Path.cwd() / 'media' / 'audio_file' / f'userid_{user_id}'
        if not file_path.is_dir():
            file_path.mkdir(parents=True, exist_ok=True)
        file_path_str = str(file_path) + f'/{datetime.now().strftime("%H%M%S%d%m%Y")}u.mp4'

        with open(file_path_str, 'wb') as file:
            file.write(audio.file.read())
    else:
        file_path_str = None

    chat_user = Chat(
        user_id=user_id,
        message=message_user,
        themes=themes,
        path_to_audio=file_path_str,
        message_from='US'
    )

    session.add(chat_user)

    # res_ai = await message_ai(message_user)
    res_ai = 'Drou'    # тут нужно будет подстаить текстовый ответ от AI

    chat_ai = Chat(
        user_id=user_id,
        message=res_ai,
        themes=themes,
        path_to_audio=None,   # тут нужно будет подставить путь до аудио файла от AI
        message_from='AI'
    )

    session.add(chat_ai)
    await session.commit()
    return chat_ai
