from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core import db_halper
from . import crud
from .shemas import Chat, ChatCreate

router = APIRouter(tags=['Chats'])


@router.get('/{id_chat}/', response_model=Chat)
async def get_chat(
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        id_chat: int):
    chat = await crud.get_chat(id_chat=id_chat, session=session)
    if chat:
        return chat

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.post('/', response_model=Chat, status_code=status.HTTP_201_CREATED, )
async def create_chat(
        chat_in: Annotated[ChatCreate, Depends()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
):
    return await crud.create_chat(session=session, chat_in=chat_in)


