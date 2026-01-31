"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database (using SQLite for easier setup, can switch to PostgreSQL in production)
    DATABASE_URL: str = "sqlite:///./smart_retail_cart.db"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Model
    AI_MODEL_PATH: Optional[str] = None  # Path to YOLOv8 weights, None for mock mode
    AI_CONFIDENCE_THRESHOLD: float = 0.5
    
    # MQTT Simulation
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
