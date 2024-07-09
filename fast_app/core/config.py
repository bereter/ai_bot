from os import getenv
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from pydantic import BaseModel
from typing import AsyncGenerator

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15


class Setting(BaseSettings):
    # api prefix
    api_v1_prefix: str = '/api/v1'

    # db
    db_url: str = getenv('DB_POSTGRES')
    db_echo: bool = True

    # jwt path
    auth_jwt: AuthJWT = AuthJWT()


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            max_overflow: int = 10,
            pool_size: int = 10
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


settings = Setting()

db_halper = DatabaseHelper(
    url=settings.db_url,
    echo=True,
    echo_pool=False,
    max_overflow=20,
    pool_size=50,


)
