"""Application settings and environment configuration."""

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized runtime settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "test-fastAPI"
    app_env: Literal["dev", "prod"] = "dev"
    port: int = 8000

    mongodb_url: str = Field(default="mongodb://localhost:27017/test_fastapi", alias="MONGODB_URL")
    external_api_url: str = Field(default="https://pruebareactjs.test-class.com/Api/", alias="EXTERNAL_API_URL")
    cors_allowed_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=list, alias="CORS_ALLOWED_ORIGINS"
    )

    httpx_timeout_seconds: float = Field(default=15, alias="HTTPX_TIMEOUT_SECONDS")
    httpx_retry_attempts: int = Field(default=3, alias="HTTPX_RETRY_ATTEMPTS")
    httpx_retry_backoff_ms: int = Field(default=250, alias="HTTPX_RETRY_BACKOFF_MS")
    session_ttl_hours: int = Field(default=24, alias="SESSION_TTL_HOURS")

    @field_validator("external_api_url")
    @classmethod
    def ensure_external_url_suffix(cls, value: str) -> str:
        """Ensure upstream base URL always ends in slash."""
        return value if value.endswith("/") else f"{value}/"

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: str | list[str]) -> list[str]:
        """Support comma-separated env var for CORS origins."""
        if isinstance(value, list):
            return value
        if not value:
            return []
        return [origin.strip() for origin in value.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings provider for dependency injection."""
    return Settings()
