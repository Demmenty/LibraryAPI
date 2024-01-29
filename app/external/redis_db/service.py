import redis.asyncio as aioredis
from redis.asyncio import Redis

from app.config import settings
from app.external.redis_db.schemas import RedisData


class RedisService:

    def __init__(self):
        self.pool: aioredis.ConnectionPool = None
        self.client: Redis = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def connect(self, max_connections: int = 10):
        """
        Connects to a Redis database and creates a connection pool.

        Args:
            max_connections (int, optional): The maximum number of connections to be created.
                Defaults to 10.
        """

        self.pool = aioredis.ConnectionPool.from_url(
            str(settings.REDIS_URL),
            max_connections=max_connections,
            decode_responses=True,
        )
        self.client = aioredis.Redis(connection_pool=self.pool)

    async def disconnect(self):
        """Disconnects from the Redis connection pool"""

        await self.pool.disconnect()

    async def set_key(
        self, redis_data: RedisData, *, is_transaction: bool = False
    ) -> None:
        """
        Sets the key in the Redis database with the provided RedisData object.

        Args:
            redis_data (RedisData): The RedisData object containing the key and value to be set.
            is_transaction (bool, optional): Indicates if the operation should be performed within a transaction.
                Defaults to False.
        """

        async with self.client.pipeline(transaction=is_transaction) as pipe:
            await pipe.set(redis_data.key, redis_data.value)
            if redis_data.ttl:
                await pipe.expire(redis_data.key, redis_data.ttl)
            await pipe.execute()

    async def get_by_key(self, key: str) -> str | None:
        """
        Retrieves a value from the database using the specified key.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            str | None: The value associated with the specified key, or None if not found.
        """

        value = await self.client.get(key)

        return value

    async def delete_by_key(self, key: str) -> None:
        """
        Deletes an item by key.

        Args:
            key (str): The key of the item to delete.
        """

        await self.client.delete(key)


redis_service = RedisService()
