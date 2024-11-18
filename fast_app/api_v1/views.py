from fastapi import APIRouter, HTTPException, status, Depends, Query, UploadFile, Response, Form, Body
from fastapi.security import APIKeyCookie
from typing import Annotated
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from core import db_halper

from api_v1.user import crud as crud_user
from api_v1.chats import crud as crud_chat
from api_v1.personage import crud as crud_personage
from api_v1.user.shemas import User, UserList
from api_v1.chats.shemas import Chat
from api_v1.personage.shemas import Personage
from api_v1.user.scurity import password_hash, verify_password_hash, create_access_token, verify_token, COOKIE_NAME

router_user = APIRouter(tags=['User'])
router_chats = APIRouter(tags=['Chats'])
router_personage = APIRouter(tags=['Personage'])

oauth2_cookie = APIKeyCookie(name=COOKIE_NAME)


class Themes(str, Enum):
    JR = "John_Rockefeller"
    HF = "Henry_Ford"
    TE = "Thomas_Edison"
    GG = 'Galileo_Galilei'
    LV = 'Leonardo_da_Vinci'
    AE = 'Albert_Einstein'


# проверка куки пользователя
async def check_cooke_user(
        cookie: str,
        id_user: int,
        session: AsyncSession
):
    payload = await verify_token(cookie)
    user = await crud_user.get_user(id_user=id_user, session=session)
    if user:
        if not user.verification_email:
            raise HTTPException(
                status_code=403,
                detail='You have not passed the verification by mail'
            )
        return True if payload.get('id') == user.id else False
    else:
        return False


@router_chats.get('/{id_user}/{themes}/', response_model=UserList)
async def get_user_chats(
        id_user: int,
        themes: Themes,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)],
        limit: Annotated[int | None, Query()] = 10,
        offset: Annotated[int | None, Query()] = 0,
):
    """
    Получение списока чатов пользователя

    - **id_user**: id пользователя
    - **themes**: тема списка чатов
    - **limit**: колличество сообщений которое вернется
    - **offset**: с каого сообщения выводить список. 0 это последнее сообщение
    """

    verification = await check_cooke_user(id_user=id_user, cookie=cookie, session=session)
    user_chats = await crud_user.get_user_chats(
        id_user=id_user,
        themes=themes.name,
        session=session,
        limit=limit,
        offset=offset
    )
    if user_chats and verification:
        return user_chats
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router_user.post('/login/', response_model=User)
async def signin_user(
        user_email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        response: Response,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]):
    """Вход пользователя по email и паролю"""

    user_login = await crud_user.get_user_by_email(user_email=user_email, session=session)

    if not user_login or not await verify_password_hash(password, user_login.password):
        raise HTTPException(
            status_code=400,
            detail='Incorrect email or password'
        )
    if not user_login.verification_email:
        raise HTTPException(
            status_code=403,
            detail='You have not passed the verification by mail'
        )
    token = await create_access_token(user_login)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True
    )
    return user_login


@router_user.post('/signup/', status_code=status.HTTP_201_CREATED)
async def create_user(
        username: Annotated[str, Form()],
        user_email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """Регистрация нового пользователя и отправка сообщения на почту"""

    copy_user = await crud_user.get_user_by_email(user_email=user_email, session=session)

    if copy_user:
        raise HTTPException(
            status_code=400,
            detail='User with this email exists'
        )

    password_new = await password_hash(password)

    signup = await crud_user.create_user(
        session=session,
        username=username,
        user_email=user_email,
        password=password_new
    )
    token = await create_access_token(signup)
    await crud_user.send_verify(token=token, user_email=user_email)

    if signup:
        return {'status': 'The letter was sent by email'}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router_chats.post('/', response_model=Chat, status_code=status.HTTP_201_CREATED, )
async def create_chat(
        user_id: Annotated[int, Body()],
        message_user: Annotated[str, Body()],
        themes: Annotated[Themes, Body()],
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)],
        cookie: Annotated[str, Depends(oauth2_cookie)],
        audio: UploadFile = None,
):
    """Создание и отправка сообщения AI. Вернется ответ от AI"""

    if check_cooke_user(id_user=user_id, cookie=cookie, session=session):
        return await crud_chat.create_chat(session=session,
                                           user_id=user_id,
                                           message_user=message_user,
                                           audio=audio,
                                           themes=themes.name)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router_user.get('/logout/')
async def logout_user(response: Response, cookie: Annotated[str, Depends(oauth2_cookie)]):
    """Выход пользователя из системы"""

    response.delete_cookie(key=COOKIE_NAME)
    return {'message': 'The user has successfully logged out of the application'}


@router_user.get('/verify/{token}/', response_model=User)
async def verify_user(
        token: str,
        response: Response,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """Вход пользователя через ссылку. Отдает данные пользователя"""

    payload = await verify_token(token)
    email_user = payload.get('user_email')
    user = await crud_user.get_user_by_email(user_email=email_user, session=session)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    await crud_user.user_email_veryfi(session=session, user=user)

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True
    )

    return user


@router_personage.get('/{themes}/', response_model=Personage)
async def personage_status(
        themes: Themes,
        session: Annotated[AsyncSession, Depends(db_halper.session_getter)]
):
    """Отдает статус персонажа"""

    persona = await crud_personage.get_personage(session=session, personage=themes.name)
    if persona:
        return persona
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
