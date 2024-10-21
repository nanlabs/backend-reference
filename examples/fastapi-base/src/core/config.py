import os

from starlette.config import Config

ROOT_DIR = os.getcwd()
_config = Config(os.path.join(ROOT_DIR, ".env"))

# API info
APP_VERSION = "0.0.1"
APP_NAME = "Base API"

# Env vars
IS_DEBUG: bool = _config("IS_DEBUG", cast=bool, default=True)

# Allow hosts
ALLOWED_CORS_HOSTS = ["*"]
ALLOWED_CORS_METHODS = ["*"]
ALLOWED_CORS_HEADERS = ["*"]
