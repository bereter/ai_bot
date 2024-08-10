import smtplib
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User, Chat
from .shemas import UserCreate
from sqlalchemy.orm import selectinload, contains_eager
from email.message import EmailMessage
from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


# получение пользователя по id
async def get_user(session: AsyncSession, id_user: int) -> User | None:
    return await session.get(User, id_user)


# получение пользователя по email
async def get_user_by_email(session: AsyncSession, user_email: str) -> User | None:
    stmt = select(User).filter_by(user_email=user_email)
    result: Result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    return user


# создание пользователя
async def create_user(session: AsyncSession, username: str, user_email: str, password: str) -> User:
    user = User(username=username, user_email=user_email, password=password)
    session.add(user)
    await session.commit()
    return user


# получение чатов пользователя
async def get_user_chats(session: AsyncSession, id_user: int, limit: int, offset: int) -> User | None:
    subq = (
        select(Chat.id)
        .filter(Chat.user_id == User.id)
        .order_by(Chat.datetime.desc())
        .limit(limit)
        .offset(offset)
        .scalar_subquery()
        .correlate(User)
    )
    stmt = (
        select(User)
        .filter_by(id=id_user)
        .outerjoin(Chat, Chat.id.in_(subq))
        .options(contains_eager(User.chats))
    )
    result: Result = await session.execute(stmt)
    user_chats = result.unique().scalars().one_or_none()
    return user_chats


async def send_verify(token: str, user_email: str) -> None:

    msg = EmailMessage()
    msg['Subject'] = 'Email subject'
    msg['From'] = getenv('EMAIL_SEND')
    msg['To'] = user_email
    msg.set_content(
        f'''
        verify account
        http://localhost:8000/user/verify/{token}
        ''',
    )
    with smtplib.SMTP_SSL('smtp.yandex.com', 465) as smtp:
        smtp.login(getenv('EMAIL_SEND'), getenv('EMAIL_PASSWORD'))
        smtp.send_message(msg)


