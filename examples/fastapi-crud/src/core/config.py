from functools import lru_cache
from os import getenv
from typing import List, Optional

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings
from pydantic.error_wrappers import ValidationError


class ApiSettings(BaseSettings):
    version: Optional[str] = "Default Mode"
    debug: Optional[bool] = True
    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8000
    allow_origins: Optional[List[str]] = ["*"]
    allow_credentials: Optional[List[str]] = ["*"]
    allow_methods: Optional[List[str]] = ["*"]
    allow_headers: Optional[List[str]] = ["*"]
    title: Optional[str] = "FastApi Poc"

    class Config:
        env_file = ".env"


class DbBaseSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_name: str
    pgadmin_default_email: str
    pgadmin_default_password: str


class DbSettings(DbBaseSettings):
    class Config:
        env_file = ".env.database"


class Settings:

    @lru_cache
    def get_api_settings() -> ApiSettings:
        return ApiSettings()

    @lru_cache
    def get_db_settings() -> DbSettings:
        """First try to get env values from .env file.
        Pydantic will only check the current working directory and won't check any parent directories for the .env.database file.
        If pydantic does not find the file dotenv library will search the file in parent directories,
        If it finds the file the values will be loaded and then set with os.getenv method.
        """
        try:
            return DbSettings()
        except ValidationError:
            db_env_file_path = find_dotenv(".env.database", True)
            load_dotenv(db_env_file_path)
            return DbBaseSettings(
                postgres_host="localhost",
                postgres_port=getenv("POSTGRES_PORT"),
                postgres_user=getenv("POSTGRES_USER"),
                postgres_password=getenv("POSTGRES_PASSWORD"),
                postgres_name=getenv("POSTGRES_NAME"),
                pgadmin_default_email=getenv("PGADMIN_DEFAULT_EMAIL"),
                pgadmin_default_password=getenv("PGADMIN_DEFAULT_PASSWORD"),
            )
