from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
from typing import Generator
import os


def _create_engine(database_url: str):
    # special args for sqlite
    if database_url.startswith("sqlite"):
        return create_engine(database_url, echo=False, connect_args={"check_same_thread": False})
    return create_engine(database_url, echo=False)


# initialize engine from settings (can be overridden in tests)
DATABASE_URL = os.getenv("DATABASE_URL", settings.database_url)
engine = _create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def override_database(url: str):
    """Override module-level engine (used in tests)."""
    global engine
    engine = _create_engine(url)


def get_engine():
    return engine
