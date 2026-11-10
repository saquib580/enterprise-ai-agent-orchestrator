"""Validated application settings loaded from environment variables."""

from functools import lru_cache
from typing import Literal
from urllib.parse import quote_plus

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration with secret-safe values."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Enterprise AI Agent Orchestrator"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    secret_key: SecretStr = SecretStr("development-only-change-before-deployment")
    database_host: str = "127.0.0.1"
    database_port: int = 3306
    database_name: str = "enterprise_ai_orchestrator"
    database_user: str = "enterprise_app"
    database_password: SecretStr = SecretStr("")
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_pool_timeout: int = 30
    database_pool_recycle: int = 1800
    database_echo: bool = False
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    openai_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None
    ai_default_model: str | None = None
    ai_max_concurrent_executions: int = 10
    ai_execution_timeout_seconds: int = 120
    log_level: str = "INFO"

    @field_validator("api_v1_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        """Require a leading slash and normalize the trailing slash."""
        if not value.startswith("/"):
            raise ValueError("API prefix must start with '/'")
        return value.rstrip("/")

    @field_validator("database_pool_size", "ai_max_concurrent_executions")
    @classmethod
    def validate_positive_limits(cls, value: int) -> int:
        """Reject invalid pool and concurrency limits."""
        if value < 1:
            raise ValueError("Value must be greater than zero")
        return value

    @property
    def database_url(self) -> str:
        """Build a URL-encoded asynchronous MySQL connection URL."""
        username = quote_plus(self.database_user)
        password = quote_plus(self.database_password.get_secret_value())
        return (
            f"mysql+aiomysql://{username}:{password}@"
            f"{self.database_host}:{self.database_port}/"
            f"{self.database_name}?charset=utf8mb4"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return one validated settings object per process."""
    return Settings()
