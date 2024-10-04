from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CACHE_EXPIRE: int = 300
    CACHE_BACKEND: str = 'memory'
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

settings = Settings()