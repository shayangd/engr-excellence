from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "User Management API"
    debug: bool = True
    database_url: str = "sqlite:///./users.db"
    
    class Config:
        env_file = ".env"


settings = Settings()