import hashlib
import os
from fastapi import Request, Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis


class RedisCache:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.prefix = "books-cache"

    @staticmethod
    def custom_key_builder(
        func, namespace, request: Request, response: Response, *args, **kwargs
    ):
        cachekey = hashlib.md5(
            f"{namespace}:{request.method}:{request.url.path}:{request.url.query}".encode()
        ).hexdigest()
        print(cachekey)
        return f"{namespace}:{cachekey}"
        # return f"{namespace}:{request.method}:{request.url.path}:{request.url.query}"

    async def init(self):
        redis = aioredis.from_url(self.redis_url)
        FastAPICache.init(
            RedisBackend(redis), prefix=self.prefix, key_builder=self.custom_key_builder
        )
        return redis
