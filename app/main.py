from contextlib import asynccontextmanager
from typing import AsyncGenerator

import click
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.books.models import Base  # -> migrations/env.py
from app.books.router import router as books_router
from app.commands import createadmin
from app.config import app_configs, settings
from app.external.redis_db.service import redis_service
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    await redis_service.connect()

    yield

    await redis_service.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    """Check if the server is up and running"""

    return {"status": "ok"}


@click.group()
def cli():
    pass


cli.add_command(createadmin)


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["User Management"])
app.include_router(books_router, prefix="/books", tags=["Book Management"])


if __name__ == "__main__":
    import uvicorn

    cli()
    uvicorn.run(app)
