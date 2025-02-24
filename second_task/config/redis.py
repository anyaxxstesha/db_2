from typing import AsyncGenerator
import redis.asyncio as redis
from second_task.config.settings import REDIS_HOST, REDIS_PORT


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    async with redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}") as redis_conn:
        yield redis_conn
