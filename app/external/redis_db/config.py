from pydantic_settings import BaseSettings


class Config(BaseSettings):
    REDIS_URL: str = "redis://redis:6379"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    API_REDIS_HOST: str = "api-redis"


redis_config = Config()
