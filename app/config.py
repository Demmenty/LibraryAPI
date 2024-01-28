from enum import Enum
from typing import Any

from dotenv import find_dotenv, load_dotenv
from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class Environment(str, Enum):
    """ Класс с константами окружения приложения """

    LOCAL = "LOCAL"
    STAGING = "STAGING"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        """Проверяет, является ли окружение отладочным."""
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        """Проверяет, является ли окружение тестовым."""
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        """Проверяет, развернуто ли окружение."""
        return self in (self.STAGING, self.PRODUCTION)


class Config(BaseSettings):
    """Класс основных настроек приложения"""

    DATABASE_URL: PostgresDsn
    SITE_DOMAIN: str

    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"

    model_config = SettingsConfigDict(case_sensitive=True)

    @model_validator(mode="after")
    def validate_sentry_non_local(self) -> "Config":
        """Проверяет, что DSN для Sentry установлен, если приложение в production."""

        if self.ENVIRONMENT.is_deployed and not self.SENTRY_DSN:
            raise ValueError("Sentry is not set")

        return self


settings = Config()

app_configs: dict[str, Any] = {"title": "Library Management API"}

if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"
