"""Environment-based application settings."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from the environment and an optional `.env` file.

    Environment variables use the field names below (case-insensitive), for
    example ``DATABASE_URL`` and ``API_PREFIX``. Values already set in the
    process environment take precedence over `.env`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Chronicle Atlas"
    environment: str = "development"
    database_url: str = "sqlite:///./chronicle_atlas.db"
    api_prefix: str = "/api"

    @field_validator("app_name", "environment", "database_url", "api_prefix")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        """Reject empty configuration values after trimming whitespace."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped

    @field_validator("api_prefix")
    @classmethod
    def normalize_prefix(cls, value: str) -> str:
        """Ensure the API prefix is absolute and has no trailing slash."""
        prefix = value if value.startswith("/") else f"/{value}"
        return prefix.rstrip("/") or "/"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings instance."""
    return Settings()
