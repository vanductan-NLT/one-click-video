from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "One Click Video"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@db:5432/one_click_video"
    
    # Redis / Queue
    REDIS_URL: str = "redis://redis:6379/0"
    
    # AWS / S3 (For M0.2 but defined now)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "ocv-storage"
    S3_ENDPOINT_URL: Optional[str] = None
    
    # AI APIs
    GEMINI_API_KEY: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "yoursupersecretkeyhere"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
