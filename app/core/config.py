from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/finance"
    secret_key: str = "change_me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    class Config:
        env_file = ".env"


settings = Settings()

# Enforce non-default SECRET_KEY in non-dev environments
_db_url = os.getenv("DATABASE_URL", settings.database_url)
if settings.secret_key in (None, "change_me") and not _db_url.startswith("sqlite"):
    raise RuntimeError("SECRET_KEY is not set properly. Set SECRET_KEY env var before running in production.")
