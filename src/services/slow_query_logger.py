"""
Slow Query Logger
==================
Automatically logs queries exceeding threshold
"""

import logging
import time
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)


def log_slow_query(threshold_ms: int = 300, query_type: str = "general"):
    """
    Decorator to log slow queries

    Args:
        threshold_ms: Log queries slower than this (milliseconds)
        query_type: Type of query (e.g., 'redis', 'monday', 'search', 'database')

    Usage:
        @log_slow_query(threshold_ms=500, query_type="monday")
        def get_items():
            return monday.api_call()
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed_ms = (time.time() - start_time) * 1000

                if elapsed_ms > threshold_ms:
                    logger.warning(
                        f"Slow {query_type} query detected: {func.__name__} "
                        f"took {elapsed_ms:.2f}ms (threshold: {threshold_ms}ms)"
                    )

        return wrapper

    return decorator


class SlowQueryContext:
    """
    Context manager for logging slow operations

    Usage:
        with SlowQueryContext("Redis GET", threshold_ms=100):
            value = redis.get(key)
    """

    def __init__(self, operation: str, threshold_ms: int = 300):
        self.operation = operation
        self.threshold_ms = threshold_ms
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_ms = (time.time() - self.start_time) * 1000

        if elapsed_ms > self.threshold_ms:
            logger.warning(
                f"Slow operation: {self.operation} "
                f"took {elapsed_ms:.2f}ms (threshold: {self.threshold_ms}ms)"
            )

        return False  # Don't suppress exceptions


# Global slow query tracker
class SlowQueryTracker:
    """Track slow queries for monitoring and alerting"""

    def __init__(self):
        self.slow_queries = []
        self.max_tracked = 100  # Keep last 100 slow queries

    def record(self, query_type: str, operation: str, duration_ms: float):
        """Record a slow query"""
        self.slow_queries.append(
            {
                "type": query_type,
                "operation": operation,
                "duration_ms": duration_ms,
                "timestamp": time.time(),
            }
        )

        # Keep only recent queries
        if len(self.slow_queries) > self.max_tracked:
            self.slow_queries = self.slow_queries[-self.max_tracked :]

    def get_summary(self):
        """Get summary of slow queries"""
        if not self.slow_queries:
            return {"total": 0, "by_type": {}, "recent": []}

        by_type = {}
        for query in self.slow_queries:
            query_type = query["type"]
            by_type[query_type] = by_type.get(query_type, 0) + 1

        return {
            "total": len(self.slow_queries),
            "by_type": by_type,
            "recent": self.slow_queries[-10:],  # Last 10
            "slowest": sorted(self.slow_queries, key=lambda x: x["duration_ms"], reverse=True)[:5],
        }


# Global tracker instance
slow_query_tracker = SlowQueryTracker()
