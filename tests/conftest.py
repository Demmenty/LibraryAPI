import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import settings
from app.external.redis_db.service import RedisService
from app.main import Base, app

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="function")
def test_client():
    return TestClient(app)


@pytest.fixture()
async def redis_service():
    async with RedisService() as client:
        await client.connect()
        yield client
        await client.disconnect()


@pytest.fixture(autouse=True, scope="function")
async def clear_db():
    try:
        engine = create_async_engine(settings.DATABASE_URL, future=True)
        session = AsyncSession(engine)
        connection = session.connection()
        print("Cleaning tables...")
        for table in Base.metadata.tables:
            await session.execute(text(f'TRUNCATE "{table}" CASCADE'))

        await session.commit()
        connection.close()
        print("Tables cleaned")

    except Exception as err:
        print("Clear_db error:", err)

    yield
