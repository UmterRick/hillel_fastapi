from redis import asyncio as aioredis

from src.base_settings import base_settings


class RedisClient:
    redis: aioredis.Redis = None

    @classmethod
    def get_or_create(cls) -> aioredis.Redis:
        return cls.redis or aioredis.from_url(
            f"redis://{base_settings.redis.host}:{base_settings.redis.port}",
            decode_responses=True
        )


def get_redis_client() -> aioredis.Redis:
    return RedisClient.get_or_create()