from passlib.context import CryptContext
from jose import jwt
from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

COOKIE_NAME = 'Authorization'


# хеширование пароля
async def password_hash(password):
    return pwd_context.hash(password)


# расшифровка пароля
async def verify_password_hash(password, verify_password):
    return pwd_context.verify(password, verify_password)


# создание токена
async def create_access_token(user):
    try:
        payload = {
            'username': user.username,
            'user_email': user.user_email,

        }
        return jwt.encode(payload, key=getenv('JWT_SECRET'), algorithm=getenv('ALGORITHM'))
    except Exception as ex:
        print(ex)
        raise ex


# расшифровка токена
async def verify_token(token):
    try:
        payload = jwt.decode(token, key=getenv('JWT_SECRET'))
        return payload
    except Exception as ex:
        print(str(ex))
        raise ex

