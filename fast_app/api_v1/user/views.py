from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from core import db_halper

from . import crud
from .shemas import User, UserCreate

router = APIRouter(tags=['User'])


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def post_user(
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        user_in: Annotated[UserCreate, Depends()]):
    return await crud.create_user(session=session, user_create=user_in)


@router.get('/{id_user}/', response_model=User)
async def get_user(
        id_user: int,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]):
    user = await crud.get_user(id_user=id_user, session=session)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
