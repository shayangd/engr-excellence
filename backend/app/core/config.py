from pydantic_settings import BaseSettings
from typing import Optional


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
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
