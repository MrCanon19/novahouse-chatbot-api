"""
Enhanced Rate Limiting Middleware
Per-endpoint and per-user rate limiting with Redis backend
"""

import functools
import hashlib
import os
from datetime import datetime, timedelta

from flask import jsonify, request
from redis import Redis

# Env toggle helpers
def is_rate_limit_disabled() -> bool:
    return os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "false"


# Redis connection
redis_client = None
try:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = Redis.from_url(redis_url, decode_responses=True)
    redis_client.ping()
except Exception:
    redis_client = None  # Fallback to in-memory

# In-memory fallback storage
_memory_store = {}


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded"""


class DummyLimiter:
    """No-op limiter used when RATE_LIMIT_ENABLED=false"""

    def limit(self, *args, **kwargs):
        def decorator(f):
            return f

        return decorator


def get_rate_limit_key(identifier, endpoint):
    """Generate a unique key for rate limiting"""
    return f"ratelimit:{endpoint}:{identifier}"


def check_rate_limit(key, limit, window):
    """
    Check if rate limit is exceeded

    Args:
        key: Unique identifier for this rate limit
        limit: Maximum number of requests allowed
        window: Time window in seconds

    Returns:
        tuple: (allowed, remaining, reset_time)
    """
    if redis_client:
        return _check_rate_limit_redis(key, limit, window)
    else:
        return _check_rate_limit_memory(key, limit, window)


def _check_rate_limit_redis(key, limit, window):
    """Redis-based rate limiting"""
    now = datetime.utcnow()
    window_start = now - timedelta(seconds=window)

    pipe = redis_client.pipeline()

    # Remove old entries
    pipe.zremrangebyscore(key, 0, window_start.timestamp())

    # Count current requests
    pipe.zcard(key)

    # Add current request
    pipe.zadd(key, {str(now.timestamp()): now.timestamp()})

    # Set expiry
    pipe.expire(key, window)

    results = pipe.execute()
    current_count = results[1]

    allowed = current_count < limit
    remaining = max(0, limit - current_count - 1)
    reset_time = int((now + timedelta(seconds=window)).timestamp())

    return allowed, remaining, reset_time


def _check_rate_limit_memory(key, limit, window):
    """In-memory fallback rate limiting"""
    now = datetime.utcnow()
    window_start = now - timedelta(seconds=window)

    if key not in _memory_store:
        _memory_store[key] = []

    # Remove old entries
    _memory_store[key] = [ts for ts in _memory_store[key] if ts > window_start]

    current_count = len(_memory_store[key])
    allowed = current_count < limit

    if allowed:
        _memory_store[key].append(now)

    remaining = max(0, limit - current_count - 1)
    reset_time = int((now + timedelta(seconds=window)).timestamp())

    return allowed, remaining, reset_time


def get_client_identifier():
    """Get unique identifier for the client (IP + User-Agent hash)"""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")

    # Hash for privacy
    identifier = hashlib.md5(f"{ip}:{user_agent}".encode()).hexdigest()
    return identifier


def rate_limit(limit_per_hour=100, endpoint_name=None):
    """
    Decorator for rate limiting endpoints

    Usage:
        @rate_limit(limit_per_hour=200, endpoint_name='chatbot')
        def chat():
            ...
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Check if rate limiting is enabled
            if not os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true":
                return f(*args, **kwargs)

            # Get endpoint name
            endpoint = endpoint_name or request.endpoint or f.__name__

            # Get client identifier
            client_id = get_client_identifier()

            # Check rate limit
            key = get_rate_limit_key(client_id, endpoint)
            window = 3600  # 1 hour in seconds

            allowed, remaining, reset_time = check_rate_limit(key, limit_per_hour, window)

            # Add rate limit headers
            response_headers = {
                "X-RateLimit-Limit": str(limit_per_hour),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(reset_time),
            }

            if not allowed:
                response = jsonify(
                    {
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Limit: {limit_per_hour} per hour",
                        "retry_after": reset_time,
                    }
                )
                response.status_code = 429
                for key, value in response_headers.items():
                    response.headers[key] = value
                return response

            # Execute function
            result = f(*args, **kwargs)

            # Add headers to response
            if hasattr(result, "headers"):
                for key, value in response_headers.items():
                    result.headers[key] = value

            return result

        return wrapper

    return decorator


# Predefined rate limit decorators for common endpoints
rate_limit_chatbot = rate_limit(limit_per_hour=200, endpoint_name="chatbot")
rate_limit_admin = rate_limit(limit_per_hour=50, endpoint_name="admin")
rate_limit_upload = rate_limit(limit_per_hour=10, endpoint_name="upload")
rate_limit_api = rate_limit(limit_per_hour=100, endpoint_name="api")
