from asyncio import sleep

from app.external.redis_db.schemas import RedisData


class TestRedisService:

    async def test_set_and_get_key(self, redis_service):
        data = RedisData(key="test_key", value="test_value", ttl=10)

        await redis_service.set_key(data)
        value = await redis_service.get_by_key("test_key")

        assert value == "test_value"

    async def test_get_by_nonexistent_key(self, redis_service):
        result = await redis_service.get_by_key("nonexistent_key")

        assert result is None

    async def test_delete_by_key(self, redis_service):
        data = RedisData(key="test_key", value="test_value", ttl=10)

        await redis_service.set_key(data)
        await redis_service.delete_by_key("test_key")
        result = await redis_service.get_by_key("test_key")

        assert result is None

    async def test_delete_by_nonexistent_key(self, redis_service):
        await redis_service.delete_by_key("nonexistent_key")

        assert True

    async def test_set_key_with_ttl(self, redis_service):
        data = RedisData(key="test_key", value="test_value", ttl=3)

        await redis_service.set_key(data)
        ttl = await redis_service.client.ttl(data.key)

        assert ttl == data.ttl

        await sleep(data.ttl)
        ttl = await redis_service.client.ttl(data.key)
        result = await redis_service.get_by_key(data.key)

        assert ttl <= 0
        assert result is None
