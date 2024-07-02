from os import getenv
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Setting(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    db_url: str = getenv('DB_POSTGRES')
    db_echo: bool = True


settings = Setting()

