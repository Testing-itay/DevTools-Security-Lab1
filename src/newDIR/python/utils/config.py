"""Configuration management using environment variables and Pydantic."""

import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")
    sentry_dsn: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)
    anthropic_api_key: Optional[str] = Field(default=None)
    database_url: str = Field(default="postgresql://localhost:5432/devtools")
    redis_url: str = Field(default="redis://localhost:6379/0")
    mongo_uri: str = Field(default="mongodb://localhost:27017")

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""
        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            sentry_dsn=os.getenv("SENTRY_DSN"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            database_url=os.getenv("DATABASE_URL", "postgresql://localhost:5432/devtools"),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            mongo_uri=os.getenv("MONGO_URI", "mongodb://localhost:27017"),
        )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings.from_env()
