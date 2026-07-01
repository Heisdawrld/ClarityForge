from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    ENVIRONMENT: str = Field(default="development", alias="ENVIRONMENT")
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])

    # Database
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/clarityforge")

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # Authentication
    SECRET_KEY: str = Field(default="change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI Providers
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # AI Defaults
    DEFAULT_AI_PROVIDER: str = "openai"
    DEFAULT_MODEL: str = "gpt-4-turbo-preview"

    # Tavily Search
    TAVILY_API_KEY: str | None = None

    # Sentry
    SENTRY_DSN: str | None = None

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
