import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AeroTwin"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: Optional[str] = None
    
    # AI Config Placeholders
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Maps Config Placeholders
    CESIUM_ION_TOKEN: Optional[str] = None
    MAPBOX_ACCESS_TOKEN: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            ".env"
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
