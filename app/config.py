from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "contentforge.db"


class Settings(BaseSettings):
    APP_NAME: str = "ContentForge"
    SECRET_KEY: str = "change-this-secret-key-in-production"
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = f"sqlite+aiosqlite:///{DB_PATH}"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
