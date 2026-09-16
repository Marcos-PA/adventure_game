from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/database_name"
    FRONTEND_URL: str = "http://localhost:3000"
    OPENAI_API_KEY: str = "your_openai_api_key_here"
    SECRET_KEY: str = "your_secret_key_here"
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    ALLOWED_ORIGINS: List[str]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def split_allowed_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()