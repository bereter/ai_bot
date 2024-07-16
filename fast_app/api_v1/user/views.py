from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from core import db_halper

from . import crud
from .shemas import User, UserCreate, UserList

router = APIRouter(tags=['User'])


@router.get('/{id_user}/', response_model=UserList)
async def get_user_chats(
        id_user: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        limit: Annotated[int | None, Query()] = 10,
        offset: Annotated[int | None, Query()] = 0
        ):
    user = await crud.get_user_chats(id_user=id_user, session=session, limit=limit, offset=offset)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.post('/{user_email}/', response_model=User)
async def get_user(
        password: str,
        user_email: str,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]):
    user = await crud.get_user_by_email(user_email=user_email, password=password, session=session)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def post_user(
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        user_in: Annotated[UserCreate, Depends()]):
    return await crud.create_user(session=session, user_create=user_in)




