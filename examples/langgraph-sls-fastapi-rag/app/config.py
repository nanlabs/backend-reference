
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .secrets import SecretsResolver

secrets = SecretsResolver()


class AppSettings(BaseSettings):
    title: str = Field(alias="APP_TITLE", default="NaNLabs LangGraph FastAPI RAG POC")
    version: str = Field(alias="APP_VERSION", default="0.1.2")
    stage: str = Field(alias="STAGE", default="local")


class AWSSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    region: str = Field(alias="AWS_REGION", default="us-east-1")
    s3_bucket_name: str | None = Field(alias="AWS_S3_BUCKET_NAME", default=None)
    s3_endpoint_url: str | None = Field(alias="AWS_S3_ENDPOINT_URL", default=None)
    s3_signed_url_expiration: int | None = Field(alias="AWS_S3_SIGNED_URL_EXPIRATION", default=None)

class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    aws: AWSSettings = AWSSettings()


settings = Settings()
