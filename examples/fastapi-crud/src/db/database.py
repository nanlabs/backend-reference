from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from core.config import DbBaseSettings, Settings

# Get DB credentials from .env.database file
DB_CREDENTIALS: DbBaseSettings = Settings.get_db_settings()

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (
    DB_CREDENTIALS.postgres_user,
    DB_CREDENTIALS.postgres_password,
    DB_CREDENTIALS.postgres_host,
    DB_CREDENTIALS.postgres_port,
    DB_CREDENTIALS.postgres_name,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
