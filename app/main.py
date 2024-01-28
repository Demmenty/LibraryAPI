from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging
import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.books.models import Base  # -> migrations/env.py
from app.books.router import router as books_router
from app.config import app_configs, settings
from app.external.redis_db.service import redis_service
from app.users.router import router as users_router
import click
from app.commands import createadmin


# Установка уровня логирования SQLalchemy
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    await redis_service.connect()

    yield

    await redis_service.disconnect()


""" Экземпляр FastAPI-приложения с настроенными app_configs и lifespan """
app = FastAPI(**app_configs, lifespan=lifespan)


"""
Добавляет middleware CORS в FastAPI-приложение с указанными настройками.
Это позволяет предотвратить блокировку запросов между разными источниками и 
обеспечивает безопасное взаимодействие между ними.
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

"""
sentry_sdk - это инструмент мониторинга и отслеживания ошибок в приложениях. 
Помогает быстро находить и исправлять проблемы в производственной среде.
"""
if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    """Конечная точка для проверки состояния приложения."""

    return {"status": "ok"}


"""Добавление команд"""
@click.group()
def cli():
    pass

cli.add_command(createadmin)

"""Подключение роутеров"""
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["User Management"])
app.include_router(books_router, prefix="/books", tags=["Book Management"])


""" Запуск приложения """
if __name__ == "__main__":
    import uvicorn

    cli()
    uvicorn.run(app)
