"""
Rate Limiting & Security Middleware
"""

import time
from collections import defaultdict
from datetime import datetime
from functools import wraps

from flask import jsonify, request


# Simple in-memory rate limiter (use Redis in production)
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.cleanup_interval = 3600  # 1 hour
        self.last_cleanup = time.time()

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """Check if request is allowed"""
        now = time.time()

        # Cleanup old entries periodically
        if now - self.last_cleanup > self.cleanup_interval:
            self._cleanup()
            self.last_cleanup = now

        # Get requests for this key
        requests = self.requests[key]

        # Remove expired requests
        cutoff = now - window_seconds
        requests[:] = [req_time for req_time in requests if req_time > cutoff]

        # Check if under limit
        if len(requests) < max_requests:
            requests.append(now)
            return True

        return False

    def _cleanup(self):
        """Remove old entries to prevent memory leak"""
        now = time.time()
        keys_to_delete = []

        for key, requests in self.requests.items():
            # Remove requests older than 1 hour
            requests[:] = [req_time for req_time in requests if now - req_time < 3600]
            if not requests:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.requests[key]

    def get_remaining(self, key: str, max_requests: int, window_seconds: int) -> int:
        """Get remaining requests"""
        now = time.time()
        cutoff = now - window_seconds
        requests = self.requests.get(key, [])
        active_requests = [req_time for req_time in requests if req_time > cutoff]
        return max(0, max_requests - len(active_requests))


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(max_requests=100, window_seconds=60):
    """
    Rate limit decorator

    Usage:
        @rate_limit(max_requests=10, window_seconds=60)  # 10 req/min
        def my_endpoint():
            ...
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Use IP address as key
            key = f"rate_limit:{request.remote_addr}:{f.__name__}"

            if not rate_limiter.is_allowed(key, max_requests, window_seconds):
                remaining = rate_limiter.get_remaining(key, max_requests, window_seconds)
                return (
                    jsonify(
                        {
                            "error": "Rate limit exceeded",
                            "message": "Too many requests. Try again later.",
                            "retry_after": window_seconds,
                        }
                    ),
                    429,
                )

            # Add rate limit headers
            response = f(*args, **kwargs)
            if isinstance(response, tuple):
                response_obj, status_code = response[0], response[1]
            else:
                response_obj, status_code = response, 200

            # Add headers if response is a Flask Response object
            if hasattr(response_obj, "headers"):
                remaining = rate_limiter.get_remaining(key, max_requests, window_seconds)
                response_obj.headers["X-RateLimit-Limit"] = str(max_requests)
                response_obj.headers["X-RateLimit-Remaining"] = str(remaining)
                response_obj.headers["X-RateLimit-Reset"] = str(int(time.time() + window_seconds))

            return response if isinstance(response, tuple) else (response_obj, status_code)

        return wrapped

    return decorator


def require_api_key(f):
    """
    Require API key for endpoint

    Usage:
        @require_api_key
        def admin_endpoint():
            ...
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        import os

        api_key = os.getenv("API_KEY") or os.getenv("ADMIN_API_KEY")
        if not api_key:
            # If no API key configured, allow access (development mode)
            return f(*args, **kwargs)

        # Check for API key in headers
        provided_key = request.headers.get("X-API-Key") or request.headers.get("X-ADMIN-API-KEY")

        if not provided_key or provided_key != api_key:
            return jsonify({"error": "Unauthorized", "message": "Valid API key required"}), 401

        return f(*args, **kwargs)

    return wrapped


def log_request(f):
    """
    Log all requests to endpoint

    Usage:
        @log_request
        def my_endpoint():
            ...
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        # Log request
        print(
            f"""
        ╔══════════════════════════════════════════════════════════
        ║ REQUEST LOG
        ╠══════════════════════════════════════════════════════════
        ║ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ║ IP: {request.remote_addr}
        ║ Method: {request.method}
        ║ Path: {request.path}
        ║ User-Agent: {request.headers.get('User-Agent', 'N/A')}
        ║ Function: {f.__name__}
        ╚══════════════════════════════════════════════════════════
        """
        )

        start_time = time.time()
        response = f(*args, **kwargs)
        duration = (time.time() - start_time) * 1000  # ms

        # Log response
        status = response[1] if isinstance(response, tuple) else 200
        print(f"  ✅ Response: {status} ({duration:.2f}ms)")

        return response

    return wrapped


def cors_headers(f):
    """Add CORS headers to response"""

    @wraps(f)
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)

        if isinstance(response, tuple):
            response_obj, status_code = response[0], response[1]
        else:
            response_obj, status_code = response, 200

        # Add CORS headers if response is a Flask Response object
        if hasattr(response_obj, "headers"):
            response_obj.headers["Access-Control-Allow-Origin"] = "*"
            response_obj.headers["Access-Control-Allow-Methods"] = (
                "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            )
            response_obj.headers["Access-Control-Allow-Headers"] = (
                "Content-Type, Authorization, X-API-Key"
            )

        return response if isinstance(response, tuple) else (response_obj, status_code)

    return wrapped
