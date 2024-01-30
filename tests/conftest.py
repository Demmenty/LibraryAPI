import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.config import settings
from app.main import Base, app


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture()
def test_client():
    return TestClient(app)


@pytest.fixture()
async def db_session():
    engine = create_async_engine(settings.DATABASE_URL)
    session = AsyncSession(engine, expire_on_commit=False)
    yield session
    await session.close()


@pytest.fixture(autouse=True, scope="function")
async def clear_db(db_session):
    print("Clear tables...")
    try:
        connection = db_session.connection()
        for table in Base.metadata.tables:
            query = text(f'TRUNCATE "{table}" CASCADE')
            await db_session.execute(query)
        await db_session.commit()
        print("Tables cleared")
    except Exception as err:
        print("Clear_db error:", err)
    finally:
        connection.close()

    yield
