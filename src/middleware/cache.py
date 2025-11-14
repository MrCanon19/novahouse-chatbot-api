"""
Simple caching system
"""

import time
from functools import wraps
from typing import Any, Optional


class SimpleCache:
    """In-memory cache with TTL"""
    
    def __init__(self):
        self.cache = {}
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        now = time.time()
        
        # Periodic cleanup
        if now - self.last_cleanup > self.cleanup_interval:
            self._cleanup()
            self.last_cleanup = now
        
        if key in self.cache:
            value, expiry = self.cache[key]
            if expiry == 0 or now < expiry:
                return value
            else:
                del self.cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in cache with TTL (seconds)"""
        expiry = time.time() + ttl if ttl > 0 else 0
        self.cache[key] = (value, expiry)
    
    def delete(self, key: str):
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def _cleanup(self):
        """Remove expired entries"""
        now = time.time()
        keys_to_delete = []
        
        for key, (value, expiry) in self.cache.items():
            if expiry > 0 and now >= expiry:
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            del self.cache[key]
    
    def stats(self):
        """Get cache statistics"""
        total = len(self.cache)
        expired = sum(1 for _, (_, expiry) in self.cache.items() 
                     if expiry > 0 and time.time() >= expiry)
        
        return {
            'total_keys': total,
            'active_keys': total - expired,
            'expired_keys': expired
        }


# Global cache instance
cache = SimpleCache()


def cached(ttl=300, key_prefix=''):
    """
    Cache decorator
    
    Usage:
        @cached(ttl=60, key_prefix='faq')
        def get_faq_data():
            return expensive_operation()
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{f.__name__}"
            
            # Add args/kwargs to key if present
            if args or kwargs:
                import hashlib
                import json
                args_str = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
                args_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]
                cache_key = f"{cache_key}:{args_hash}"
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                print(f"✅ Cache HIT: {cache_key}")
                return cached_value
            
            # Cache miss - execute function
            print(f"❌ Cache MISS: {cache_key}")
            result = f(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapped
    return decorator


# Pre-warm cache for FAQ (static data)
def warm_faq_cache():
    """Pre-warm FAQ cache on startup"""
    try:
        from src.knowledge.novahouse_info import FAQ, PACKAGES, COMPANY_INFO
        
        cache.set('faq:all', FAQ, ttl=3600)  # 1 hour
        cache.set('packages:all', PACKAGES, ttl=3600)
        cache.set('company:info', COMPANY_INFO, ttl=3600)
        
        print("✅ FAQ cache warmed")
    except Exception as e:
        print(f"❌ Failed to warm cache: {e}")
