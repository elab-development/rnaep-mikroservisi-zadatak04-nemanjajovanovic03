from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    notification_group: str = "notification-group"
    notification_consumer: str = "notification-consumer-1"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()