from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Database
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "fastapi_db"

    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "FastAPI User Management"
    project_version: str = "1.0.0"

    # Development
    debug: bool = False

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS Settings
    allowed_origins: str = '["http://localhost:8571", "http://localhost:3000"]'

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
