"""
Redis Rate Limiter
==================
Production-ready rate limiting with Redis
Replaces in-memory RateLimiter
"""

import time
from functools import wraps
from flask import request, jsonify
from src.services.redis_service import redis_cache

class RedisRateLimiter:
    """Redis-based rate limiter with sliding window"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, key: str, limit: int, window: int) -> tuple[bool, dict]:
        """
        Check if request is allowed using sliding window algorithm
        
        Args:
            key: Unique identifier (e.g., IP address, user_id)
            limit: Maximum requests allowed
            window: Time window in seconds
        
        Returns:
            (allowed: bool, info: dict)
        """
        try:
            current_time = int(time.time())
            window_start = current_time - window
            
            # Remove old entries
            self.redis.redis_client.zremrangebyscore(key, 0, window_start)
            
            # Count current requests in window
            request_count = self.redis.redis_client.zcard(key)
            
            # Check if limit exceeded
            if request_count >= limit:
                # Get oldest request time for reset calculation
                oldest = self.redis.redis_client.zrange(key, 0, 0, withscores=True)
                reset_time = int(oldest[0][1]) + window if oldest else current_time + window
                
                return False, {
                    'limit': limit,
                    'remaining': 0,
                    'reset': reset_time
                }
            
            # Add current request
            self.redis.redis_client.zadd(key, {str(current_time): current_time})
            
            # Set expiration on key
            self.redis.redis_client.expire(key, window)
            
            return True, {
                'limit': limit,
                'remaining': limit - request_count - 1,
                'reset': current_time + window
            }
            
        except Exception as e:
            print(f"Rate limiter error: {e}")
            # On error, allow request (fail open)
            return True, {
                'limit': limit,
                'remaining': limit,
                'reset': int(time.time()) + window
            }

# Global rate limiter instance
redis_rate_limiter = RedisRateLimiter(redis_cache)

def rate_limit_redis(limit: int = 100, window: int = 60, key_func=None):
    """
    Redis rate limit decorator
    
    Args:
        limit: Maximum requests allowed
        window: Time window in seconds
        key_func: Optional function to generate custom key
    
    Usage:
        @rate_limit_redis(limit=10, window=60)
        def endpoint():
            return "Limited to 10 req/min"
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate rate limit key
            if key_func:
                key = key_func(request)
            else:
                # Default: use IP address
                key = f"rate_limit:{request.remote_addr}:{request.endpoint}"
            
            # Check rate limit
            allowed, info = redis_rate_limiter.is_allowed(key, limit, window)
            
            if not allowed:
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Limit: {limit} per {window}s',
                    'retry_after': info['reset'] - int(time.time())
                })
                response.status_code = 429
                response.headers['X-RateLimit-Limit'] = str(info['limit'])
                response.headers['X-RateLimit-Remaining'] = str(info['remaining'])
                response.headers['X-RateLimit-Reset'] = str(info['reset'])
                response.headers['Retry-After'] = str(info['reset'] - int(time.time()))
                return response
            
            # Add rate limit headers
            result = func(*args, **kwargs)
            
            # If result is a Response object, add headers
            if hasattr(result, 'headers'):
                result.headers['X-RateLimit-Limit'] = str(info['limit'])
                result.headers['X-RateLimit-Remaining'] = str(info['remaining'])
                result.headers['X-RateLimit-Reset'] = str(info['reset'])
            
            return result
        return wrapper
    return decorator
