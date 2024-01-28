from asyncio import sleep

import pytest

from app.external.redis_db.schemas import RedisData
from app.external.redis_db.service import RedisService


@pytest.fixture(autouse=True)
async def redis_service():
    async with RedisService() as client:
        await client.connect()
        yield client
        await client.disconnect()


@pytest.fixture
def mock_redis_data():
    return RedisData(key="test_key", value="test_value", ttl=10)


@pytest.mark.asyncio
async def test_set_and_get_key(redis_service, mock_redis_data: RedisData):
    async for client in redis_service:
        await client.set_key(mock_redis_data)
        value = await client.get_by_key("test_key")

        assert value == "test_value"


@pytest.mark.asyncio
async def test_get_by_nonexistent_key(redis_service):
    async for client in redis_service:
        result = await client.get_by_key("nonexistent_key")

        assert result is None


@pytest.mark.asyncio
async def test_delete_by_key(redis_service, mock_redis_data: RedisData):
    async for client in redis_service:
        await client.set_key(mock_redis_data)
        await client.delete_by_key("test_key")
        result = await client.get_by_key("test_key")

        assert result is None


@pytest.mark.asyncio
async def test_delete_by_nonexistent_key(redis_service):
    # No exception should be raised even if the key doesn't exist
    async for client in redis_service:
        await client.delete_by_key("nonexistent_key")

        assert True


@pytest.mark.asyncio
async def test_set_key_with_ttl(redis_service, mock_redis_data: RedisData):
    mock_redis_data.ttl = 3

    async for client in redis_service:
        await client.set_key(mock_redis_data)
        ttl = await client.client.ttl(mock_redis_data.key)

        assert ttl == mock_redis_data.ttl

        await sleep(mock_redis_data.ttl)
        ttl = await client.client.ttl(mock_redis_data.key)
        result = await client.get_by_key(mock_redis_data.key)

        assert ttl <= 0
        assert result is None
