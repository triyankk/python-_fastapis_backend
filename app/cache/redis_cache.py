from redis import Redis
from ..core.config import settings
import json
from typing import Any, Optional
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.default_ttl = 300  # 5 minutes

    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        try:
            return self.redis_client.setex(
                key,
                ttl or self.default_ttl,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False

    async def get(self, key: str) -> Optional[Any]:
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None

    async def delete(self, key: str) -> bool:
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False

cache = RedisCache()

def cached(ttl: int = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_value = await cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # If not in cache, execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            await cache.set(key, result, ttl)
            
            return result
        return wrapper
    return decorator
