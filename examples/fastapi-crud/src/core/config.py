from functools import lru_cache
from typing import List

from dotenv import find_dotenv, load_dotenv
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    version: str = "Default Mode"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    allow_origins: List[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]
    title: str = "FastApi Poc"

    model_config = SettingsConfigDict(env_file=".env")


class DbBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.database")

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_name: str
    pgadmin_default_email: str
    pgadmin_default_password: str

    def __init__(self) -> None:
        super().__init__()


class Settings:

    @staticmethod
    @lru_cache
    def get_api_settings() -> ApiSettings:
        return ApiSettings()

    @staticmethod
    @lru_cache
    def get_db_settings() -> DbBaseSettings:
        """First try to get env values from .env file.
        Pydantic checks the current working directory for .env.database but not
        parent directories. If the file is absent, dotenv searches parent
        directories and loads the values into the environment when it finds it.
        """
        try:
            return DbBaseSettings()
        except ValidationError:
            db_env_file_path = find_dotenv(".env.database", True)
            load_dotenv(db_env_file_path)
            return DbBaseSettings()
