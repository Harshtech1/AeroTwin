import os
from typing import Any

import yaml
from pydantic import field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    Custom settings source that loads configuration values from a YAML file
    based on the current ENVIRONMENT.
    """

    def get_field_value(self, field: Any, field_name: str) -> tuple[Any, str, bool]:
        # Not utilized because __call__ is implemented to load the whole dict
        return None, field_name, False

    def __call__(self) -> dict[str, Any]:
        env = os.environ.get("ENVIRONMENT", "development").lower()
        if env not in ["development", "testing", "production"]:
            raise ValueError(
                f"Invalid ENVIRONMENT '{env}'. "
                "Must be one of: development, testing, production"
            )

        root_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        yaml_path = os.path.join(root_dir, "configs", f"{env}.yaml")

        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Configuration file not found at: {yaml_path}")

        try:
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(
                f"Failed to parse YAML configuration file at {yaml_path}: {e}"
            ) from e

        if not isinstance(data, dict):
            raise ValueError(
                f"Configuration file at {yaml_path} "
                "must be a valid YAML mapping dictionary."
            )

        # Map nested YAML configs to flat Settings attributes
        flat_data: dict[str, Any] = {}

        # Parse 'app' block
        app_block = data.get("app", {})
        if isinstance(app_block, dict):
            if "name" in app_block:
                flat_data["PROJECT_NAME"] = app_block["name"]
            if "env" in app_block:
                flat_data["ENVIRONMENT"] = app_block["env"]
            if "debug" in app_block:
                flat_data["DEBUG"] = app_block["debug"]
            if "api_prefix" in app_block:
                flat_data["API_V1_STR"] = app_block["api_prefix"]

        # Parse 'database' block
        db_block = data.get("database", {})
        if isinstance(db_block, dict):
            if "url" in db_block:
                flat_data["DATABASE_URL"] = db_block["url"]

        # Parse 'ai' block
        ai_block = data.get("ai", {})
        if isinstance(ai_block, dict):
            if "openai_api_key" in ai_block:
                flat_data["OPENAI_API_KEY"] = ai_block["openai_api_key"]
            if "gemini_api_key" in ai_block:
                flat_data["GEMINI_API_KEY"] = ai_block["gemini_api_key"]

        # Parse 'maps' block
        maps_block = data.get("maps", {})
        if isinstance(maps_block, dict):
            if "cesium_ion_token" in maps_block:
                flat_data["CESIUM_ION_TOKEN"] = maps_block["cesium_ion_token"]
            if "mapbox_access_token" in maps_block:
                flat_data["MAPBOX_ACCESS_TOKEN"] = maps_block["mapbox_access_token"]

        return {k: v for k, v in flat_data.items() if v is not None}


class Settings(BaseSettings):
    PROJECT_NAME: str = "AeroTwin"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str | None = None

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # AI Config Placeholders
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None

    # Maps Config Placeholders
    CESIUM_ION_TOKEN: str | None = None
    MAPBOX_ACCESS_TOKEN: str | None = None

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        env = v.lower()
        if env not in ["development", "testing", "production"]:
            raise ValueError("ENVIRONMENT must be development, testing, or production")
        return env

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
            ),
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Custom loading priority:
        # 1. Environment variables (env_settings)
        # 2. .env file (dotenv_settings)
        # 3. YAML configs (YamlConfigSettingsSource)
        # 4. Defaults (init_settings)
        return (
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            init_settings,
        )


settings = Settings()
