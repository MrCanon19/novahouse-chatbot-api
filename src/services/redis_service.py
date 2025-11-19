"""
Redis Cache Service
===================
Production-ready caching with Redis
Replaces in-memory SimpleCache
"""

import json
import os
from functools import wraps
from typing import Any, Optional

import redis


class RedisCache:
    """Redis-based cache with TTL support"""

    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=True,  # Enable automatic decoding for JSON
                socket_connect_timeout=5,
                socket_timeout=5,
            )
            # Test connection
            self.redis_client.ping()
            self.enabled = True
            print(f"✅ Redis connected: {redis_url}")
        except Exception as e:
            print(f"⚠️ Redis unavailable, falling back to in-memory cache: {e}")
            self.enabled = False
            self._fallback_cache = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.enabled:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
                return None
            else:
                # Fallback to in-memory
                return self._fallback_cache.get(key)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Redis GET decode error: {e}")
            return None
        except Exception as e:
            print(f"Redis GET error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in cache with TTL (seconds)"""
        try:
            if self.enabled:
                serialized = json.dumps(value)
                self.redis_client.setex(key, ttl, serialized)
            else:
                # Fallback to in-memory (without TTL for simplicity)
                self._fallback_cache[key] = value
        except (TypeError, ValueError) as e:
            print(f"Redis SET serialization error: {e}")
        except Exception as e:
            print(f"Redis SET error: {e}")

    def delete(self, key: str):
        """Delete key from cache"""
        try:
            if self.enabled:
                self.redis_client.delete(key)
            else:
                self._fallback_cache.pop(key, None)
        except Exception as e:
            print(f"Redis DELETE error: {e}")

    def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            if self.enabled:
                return bool(self.redis_client.exists(key))
            else:
                return key in self._fallback_cache
        except Exception as e:
            print(f"Redis EXISTS error: {e}")
            return False

    def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        try:
            if self.enabled:
                return self.redis_client.incrby(key, amount)
            else:
                current = self._fallback_cache.get(key, 0)
                new_value = current + amount
                self._fallback_cache[key] = new_value
                return new_value
        except Exception as e:
            print(f"Redis INCR error: {e}")
            return 0

    def expire(self, key: str, ttl: int):
        """Set expiration on existing key"""
        try:
            if self.enabled:
                self.redis_client.expire(key, ttl)
        except Exception as e:
            print(f"Redis EXPIRE error: {e}")

    def ttl(self, key: str) -> int:
        """Get remaining TTL"""
        try:
            if self.enabled:
                return self.redis_client.ttl(key)
            else:
                return -1  # No TTL in fallback mode
        except Exception as e:
            print(f"Redis TTL error: {e}")
            return -1

    def flush_pattern(self, pattern: str):
        """Delete all keys matching pattern"""
        try:
            if self.enabled:
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
            else:
                # Fallback: delete matching keys
                to_delete = [
                    k for k in self._fallback_cache.keys() if pattern.replace("*", "") in k
                ]
                for key in to_delete:
                    del self._fallback_cache[key]
        except Exception as e:
            print(f"Redis FLUSH error: {e}")

    def get_stats(self) -> dict:
        """Get cache statistics"""
        try:
            if self.enabled:
                info = self.redis_client.info("stats")
                return {
                    "enabled": True,
                    "backend": "redis",
                    "keyspace_hits": info.get("keyspace_hits", 0),
                    "keyspace_misses": info.get("keyspace_misses", 0),
                    "total_keys": self.redis_client.dbsize(),
                    "memory_used": self.redis_client.info("memory").get("used_memory_human", "N/A"),
                }
            else:
                return {
                    "enabled": False,
                    "backend": "in-memory (fallback)",
                    "total_keys": len(self._fallback_cache),
                }
        except Exception as e:
            print(f"Redis STATS error: {e}")
            return {"enabled": False, "error": str(e)}


# Global cache instance
redis_cache = RedisCache()


def cached_redis(ttl: int = 300, key_prefix: str = "cache"):
    """
    Redis cache decorator

    Args:
        ttl: Time to live in seconds (default 5 min)
        key_prefix: Prefix for cache key

    Usage:
        @cached_redis(ttl=600, key_prefix='faq')
        def get_faq():
            return expensive_query()
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and args
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            cached_value = redis_cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function
            result = func(*args, **kwargs)

            # Store in cache
            redis_cache.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator


def warm_redis_cache():
    """Pre-warm Redis cache with frequently accessed data"""
    try:
        from src.knowledge.novahouse_info import CLIENT_REVIEWS, FAQ, PORTFOLIO, PROCESS_STEPS

        # Cache FAQ
        redis_cache.set("knowledge:faq", FAQ, ttl=3600)

        # Cache portfolio
        redis_cache.set("knowledge:portfolio", PORTFOLIO, ttl=3600)

        # Cache process
        redis_cache.set("knowledge:process", PROCESS_STEPS, ttl=3600)

        # Cache reviews
        redis_cache.set("knowledge:reviews", CLIENT_REVIEWS, ttl=3600)

        print("✅ Redis cache warmed with knowledge base data")

    except Exception as e:
        print(f"⚠️ Failed to warm cache: {e}")
