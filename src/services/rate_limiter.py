"""
Rate Limiting Middleware
Prevents spam and abuse
"""

import os
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Callable, Optional

from flask import jsonify, request


class RateLimiter:
    """
    Simple in-memory rate limiter
    For production, use Redis
    """

    def __init__(self):
        # session_id -> [(timestamp, count), ...]
        self.session_limits = defaultdict(list)
        # ip_address -> [(timestamp, count), ...]
        self.ip_limits = defaultdict(list)

    def _cleanup_old_entries(self, entries: list, window_seconds: int):
        """Remove entries older than window"""
        cutoff = time.time() - window_seconds
        return [entry for entry in entries if entry[0] > cutoff]

    def check_rate_limit(
        self,
        identifier: str,
        limit_type: str = "session",
        max_requests: int = 10,
        window_seconds: int = 60,
    ) -> tuple[bool, Optional[int]]:
        """
        Check if identifier is within rate limit

        Args:
            identifier: session_id or ip_address
            limit_type: 'session' or 'ip'
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds

        Returns:
            (is_allowed, retry_after_seconds)
        """
        # Select appropriate storage
        storage = self.session_limits if limit_type == "session" else self.ip_limits

        # Cleanup old entries
        storage[identifier] = self._cleanup_old_entries(storage[identifier], window_seconds)

        # Count requests in current window
        current_count = len(storage[identifier])

        if current_count >= max_requests:
            # Calculate retry after
            oldest_entry = storage[identifier][0][0]
            retry_after = int(window_seconds - (time.time() - oldest_entry))
            return False, retry_after

        # Add new entry
        storage[identifier].append((time.time(), 1))
        return True, None

    def clear_limits(self, identifier: Optional[str] = None):
        """Clear rate limits for identifier or all"""
        if identifier:
            self.session_limits.pop(identifier, None)
            self.ip_limits.pop(identifier, None)
        else:
            self.session_limits.clear()
            self.ip_limits.clear()


# Global rate limiter instance with Redis fallback
def get_rate_limiter():
    """Lazy load rate limiter to avoid import deadlock"""
    # Force in-memory limiter when REDIS_URL is not configured (GAE cost-saving mode)
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return RateLimiter()

    try:
        from src.services.redis_rate_limiter import RedisRateLimiter
        from src.services.redis_service import get_redis_cache

        cache = get_redis_cache()
        if cache and getattr(cache, "redis_client", None) and cache.enabled:
            # Use Redis-based rate limiter for production (multi-instance safe)
            return RedisRateLimiter()
        else:
            # Fallback to in-memory for development
            return RateLimiter()
    except BaseException as e:
        # Fallback if Redis unavailable or import fails (including SystemExit/KeyboardInterrupt)
        import traceback

        print(f"Warning: Failed to load Redis rate limiter: {e}")
        traceback.print_exc()
        return RateLimiter()


rate_limiter = None


def ensure_rate_limiter():
    """Ensure rate limiter is initialized"""
    global rate_limiter
    if rate_limiter is None:
        try:
            rate_limiter = get_rate_limiter()
        except BaseException as e:
            # Emergency fallback even on SystemExit to keep app alive
            import traceback

            print(f"ERROR: Failed to ensure rate limiter: {e}")
            traceback.print_exc()
            rate_limiter = RateLimiter()
    return rate_limiter


def rate_limit(
    max_requests: int = 10,
    window_seconds: int = 60,
    limit_by: str = "session",  # 'session' or 'ip' or 'both'
):
    """
    Decorator for rate limiting endpoints

    Args:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        limit_by: Rate limit by 'session', 'ip', or 'both'

    Example:
        @app.route('/api/chat', methods=['POST'])
        @rate_limit(max_requests=10, window_seconds=60, limit_by='session')
        def chat():
            ...
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Always lazy-load limiter to avoid None issues and import-time Redis connects
            try:
                limiter = ensure_rate_limiter()
            except Exception as e:  # Fail-open if anything goes wrong
                import traceback

                print(f"Rate limiter unavailable, allowing request: {e}")
                traceback.print_exc()
                return func(*args, **kwargs)

            # Get identifiers
            data = request.get_json() or {}
            session_id = data.get("session_id", "unknown")
            ip_address = request.remote_addr or "unknown"

            # Check session rate limit
            if limit_by in ["session", "both"]:
                allowed, retry_after = limiter.check_rate_limit(
                    session_id, "session", max_requests, window_seconds
                )
                if not allowed:
                    return (
                        jsonify(
                            {
                                "error": "Rate limit exceeded",
                                "retry_after": retry_after,
                                "limit_type": "session",
                            }
                        ),
                        429,
                    )

            # Check IP rate limit
            if limit_by in ["ip", "both"]:
                # More lenient for IP (100 requests per hour)
                ip_max = max_requests * 10
                ip_window = window_seconds * 60
                allowed, retry_after = limiter.check_rate_limit(ip_address, "ip", ip_max, ip_window)
                if not allowed:
                    return (
                        jsonify(
                            {
                                "error": "Rate limit exceeded",
                                "retry_after": retry_after,
                                "limit_type": "ip",
                            }
                        ),
                        429,
                    )

            # Rate limit passed
            return func(*args, **kwargs)

        return wrapper

    return decorator


class ConversationRateLimiter:
    """
    More sophisticated rate limiter for conversations
    Tracks message velocity and detects spam patterns
    """

    def __init__(self):
        # session_id -> [(timestamp, message), ...]
        self.conversations = defaultdict(list)

    def add_message(self, session_id: str, message: str):
        """Add message to conversation history"""
        self.conversations[session_id].append((datetime.now(timezone.utc), message))

        # Keep only last 50 messages
        if len(self.conversations[session_id]) > 50:
            self.conversations[session_id] = self.conversations[session_id][-50:]

    def is_spam(self, session_id: str, new_message: str) -> tuple[bool, str]:
        """
        Detect spam patterns

        Returns:
            (is_spam, reason)
        """
        messages = self.conversations[session_id]

        if not messages:
            return False, ""

        # Check: Too many messages in short time
        recent_messages = [
            msg for ts, msg in messages if ts > datetime.now(timezone.utc) - timedelta(seconds=30)
        ]
        if len(recent_messages) > 5:
            return True, "Too many messages in 30 seconds"

        # Check: Duplicate messages
        last_5_messages = [msg for ts, msg in messages[-5:]]
        if last_5_messages.count(new_message) >= 3:
            return True, "Duplicate message spam"

        # Check: Very short repeated messages
        if len(new_message) < 3 and len(recent_messages) > 3:
            return True, "Repeated short messages"

        # Check: All messages identical
        if len(messages) >= 3:
            last_3 = [msg for ts, msg in messages[-3:]]
            if len(set(last_3)) == 1:
                return True, "Identical messages repeated"

        return False, ""

    def clear_session(self, session_id: str):
        """Clear conversation history for session"""
        self.conversations.pop(session_id, None)


# Global conversation rate limiter
conversation_limiter = ConversationRateLimiter()
