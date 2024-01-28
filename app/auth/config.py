from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 10  # minutes

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True


auth_config = Config()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token", auto_error=False)
