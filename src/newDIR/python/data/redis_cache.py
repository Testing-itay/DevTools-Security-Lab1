"""Redis caching layer."""

from typing import Optional

import redis


def create_redis_client(host: str = "localhost", port: int = 6379, db: int = 0) -> redis.Redis:
    """Create Redis client."""
    return redis.Redis(host=host, port=port, db=db, decode_responses=True)


def cache_get(client: redis.Redis, key: str) -> Optional[str]:
    """Get value from cache."""
    return client.get(key)


def cache_set(
    client: redis.Redis,
    key: str,
    value: str,
    ttl_seconds: Optional[int] = 3600,
) -> bool:
    """Set value in cache with optional TTL."""
    return client.set(key, value, ex=ttl_seconds or None)


def cache_delete(client: redis.Redis, key: str) -> int:
    """Delete key from cache. Returns number of keys deleted."""
    return client.delete(key)
