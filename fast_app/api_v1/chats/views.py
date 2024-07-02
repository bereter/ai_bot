from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_halper
from . import crud
from .shemas import Chat, ChatCreate


router = APIRouter(tags=['Chats'])


@router.post('/', response_model=Chat, status_code=status.HTTP_201_CREATED,)
async def create_chat(
        chat_in: ChatCreate,
        session: AsyncSession = Depends(db_halper.scoped_session_dependency),
):
    return await crud.create_chats(session=session, chat_in=chat_in)


@router.get('/', response_model=list[Chat])
async def get_chats(session: AsyncSession = Depends(db_halper.scoped_session_dependency)):
    return await crud.get_chats(session=session)
