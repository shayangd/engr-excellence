from pydantic_settings import BaseSettings
from typing import Optional, List
import json
import os


class Settings(BaseSettings):
    # Database Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "fastapi_db"

    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "FastAPI User Management"
    project_version: str = "1.0.0"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8570

    # Development Settings
    debug: bool = False

    # Security Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS Settings (JSON string format)
    allowed_origins: str = '["http://localhost:8571", "http://localhost:3000"]'

    # Logging Configuration
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from JSON string"""
        try:
            return json.loads(self.allowed_origins)
        except (json.JSONDecodeError, TypeError):
            # Fallback to default origins if parsing fails
            return ["http://localhost:8571", "http://localhost:3000"]


settings = Settings()
