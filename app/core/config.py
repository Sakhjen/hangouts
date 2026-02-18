from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    # Обязательные
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_HOSTS: str = "http://localhost:3000,http://127.0.0.1:3000"
    DEBUG: bool = False
    PROJECT_NAME: str = "Hangouts API"
    VERSION: str = "1.0.0"
    
    # Database
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "hangouts_admin"
    POSTGRES_PASSWORD: str = "supersecretpassword"
    POSTGRES_DB: str = "hangouts"
    
    # SMS (добавлены ВСЕ поля из .env)
    SMS_PROVIDER: str = "smsc"
    SMS_LOGIN: str = ""
    SMS_PASSWORD: str = ""
    SMS_SENDER: str = "Hangouts"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Storage
    UPLOAD_DIR: str = "/app/uploads"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Игнорирует лишние поля
    )

    @property
    def allowed_hosts_list(self) -> List[str]:
        return [h.strip() for h in self.ALLOWED_HOSTS.split(",") if h.strip()]

settings = Settings()
