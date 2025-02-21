# core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "pyperfect.duckdb"

    class Config:
        env_file = ".env"

settings = Settings()
