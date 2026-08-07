"""Validated application configuration with environment-first precedence."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

import yaml  # type: ignore[import-untyped]
from pydantic import AnyHttpUrl, Field, field_validator, model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

Environment = Literal["development", "testing", "production"]
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """Load non-secret defaults from ``configs/<environment>.yaml``."""

    def get_field_value(self, field: Any, field_name: str) -> tuple[Any, str, bool]:
        return None, field_name, False

    def __call__(self) -> dict[str, Any]:
        environment = os.getenv("ENVIRONMENT", "development").lower()
        if environment not in {"development", "testing", "production"}:
            raise ValueError(f"Unsupported ENVIRONMENT: {environment!r}")
        path = PROJECT_ROOT / "configs" / f"{environment}.yaml"
        if not path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        try:
            document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML configuration in {path}") from exc
        if not isinstance(document, dict):
            raise ValueError(f"Configuration must be a YAML mapping: {path}")

        sections = {
            "app": {
                "name": "PROJECT_NAME",
                "env": "ENVIRONMENT",
                "debug": "DEBUG",
                "api_prefix": "API_V1_STR",
                "version": "VERSION",
            },
            "database": {
                "url": "DATABASE_URL",
                "pool_size": "DB_POOL_SIZE",
                "max_overflow": "DB_MAX_OVERFLOW",
                "pool_timeout": "DB_POOL_TIMEOUT",
                "pool_recycle": "DB_POOL_RECYCLE",
            },
            "http": {
                "cors_origins": "BACKEND_CORS_ORIGINS",
                "trusted_hosts": "TRUSTED_HOSTS",
                "gzip_minimum_size": "GZIP_MINIMUM_SIZE",
            },
        }
        result: dict[str, Any] = {}
        for section, mappings in sections.items():
            values = document.get(section, {})
            if not isinstance(values, dict):
                raise ValueError(f"Configuration section {section!r} must be a mapping")
            for yaml_key, setting_name in mappings.items():
                if yaml_key in values and values[yaml_key] is not None:
                    result[setting_name] = values[yaml_key]
        return result


class Settings(BaseSettings):
    """Runtime settings. Secrets must be supplied by env or a secrets directory."""

    PROJECT_NAME: str = "AeroTwin"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Environment = "development"
    DEBUG: bool = True
    DATABASE_URL: str | None = None
    DB_POOL_SIZE: int = Field(default=5, ge=1)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0)
    DB_POOL_TIMEOUT: float = Field(default=30.0, gt=0)
    DB_POOL_RECYCLE: int = Field(default=1800, ge=30)
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl | str] = ["*"]
    TRUSTED_HOSTS: list[str] = ["*"]
    GZIP_MINIMUM_SIZE: int = Field(default=1000, ge=0)

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        secrets_dir=os.getenv("SECRETS_DIR"),
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("API_V1_STR")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        if not value.startswith("/") or value.endswith("/"):
            raise ValueError("API_V1_STR must start, but not end, with '/'")
        return value

    @model_validator(mode="after")
    def validate_production_safety(self) -> Settings:
        if self.ENVIRONMENT == "production":
            if self.DEBUG:
                raise ValueError("DEBUG must be false in production")
            if "*" in self.BACKEND_CORS_ORIGINS:
                raise ValueError("Wildcard CORS is forbidden in production")
        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )


settings = Settings()
