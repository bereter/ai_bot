from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core import db_halper
from . import crud
from .shemas import Chat, ChatCreate

router = APIRouter(tags=['Chats'])


@router.post('/', response_model=Chat, status_code=status.HTTP_201_CREATED, )
async def create_chat(
        chat_in: Annotated[ChatCreate, Depends()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
):
    return await crud.create_chat(session=session, chat_in=chat_in)


