"""
Metrics Service - Track application metrics for monitoring
"""
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, Optional

from flask import g


class MetricsService:
    """
    Service for tracking application metrics.
    Tracks conversations, response times, errors, and LLM timeouts.
    """

    # In-memory metrics (in production, use Redis or Prometheus)
    _metrics = {
        "conversations_total": 0,
        "conversations_by_status": defaultdict(int),
        "response_times_ms": [],
        "errors_5xx": 0,
        "errors_4xx": 0,
        "llm_timeouts": 0,
        "llm_errors": 0,
        "llm_input_blocked": 0,
        "llm_output_blocked": 0,
        "rate_limit_hits": 0,
    }

    @classmethod
    def increment_conversation(cls, status: str = "success"):
        """Increment conversation counter"""
        cls._metrics["conversations_total"] += 1
        cls._metrics["conversations_by_status"][status] += 1

    @classmethod
    def record_response_time(cls, duration_ms: float):
        """Record response time"""
        cls._metrics["response_times_ms"].append(duration_ms)
        # Keep only last 1000 measurements
        if len(cls._metrics["response_times_ms"]) > 1000:
            cls._metrics["response_times_ms"] = cls._metrics["response_times_ms"][-1000:]

    @classmethod
    def increment_error(cls, status_code: int):
        """Increment error counter"""
        if 500 <= status_code < 600:
            cls._metrics["errors_5xx"] += 1
        elif 400 <= status_code < 500:
            cls._metrics["errors_4xx"] += 1

    @classmethod
    def increment_llm_timeout(cls):
        """Increment LLM timeout counter"""
        cls._metrics["llm_timeouts"] += 1

    @classmethod
    def increment_llm_error(cls):
        """Increment LLM error counter"""
        cls._metrics["llm_errors"] += 1

    @classmethod
    def increment_llm_input_blocked(cls):
        """Increment LLM input blocked counter"""
        cls._metrics["llm_input_blocked"] += 1

    @classmethod
    def increment_llm_output_blocked(cls):
        """Increment LLM output blocked counter"""
        cls._metrics["llm_output_blocked"] += 1

    @classmethod
    def increment_rate_limit(cls):
        """Increment rate limit hit counter"""
        cls._metrics["rate_limit_hits"] += 1

    @classmethod
    def get_metrics(cls) -> Dict:
        """Get all metrics"""
        response_times = cls._metrics["response_times_ms"]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        p95_response_time = (
            sorted(response_times)[int(len(response_times) * 0.95)]
            if len(response_times) >= 20
            else 0
        )

        return {
            "conversations_total": cls._metrics["conversations_total"],
            "conversations_by_status": dict(cls._metrics["conversations_by_status"]),
            "response_time_avg_ms": round(avg_response_time, 2),
            "response_time_p95_ms": round(p95_response_time, 2),
            "errors_5xx": cls._metrics["errors_5xx"],
            "errors_4xx": cls._metrics["errors_4xx"],
            "llm_timeouts": cls._metrics["llm_timeouts"],
            "llm_errors": cls._metrics["llm_errors"],
            "llm_input_blocked": cls._metrics["llm_input_blocked"],
            "llm_output_blocked": cls._metrics["llm_output_blocked"],
            "rate_limit_hits": cls._metrics["rate_limit_hits"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @classmethod
    def reset(cls):
        """Reset all metrics (for testing)"""
        cls._metrics = {
            "conversations_total": 0,
            "conversations_by_status": defaultdict(int),
            "response_times_ms": [],
            "errors_5xx": 0,
            "errors_4xx": 0,
            "llm_timeouts": 0,
            "llm_errors": 0,
            "llm_input_blocked": 0,
            "llm_output_blocked": 0,
            "rate_limit_hits": 0,
        }


# Context manager for timing requests
class RequestTimer:
    """Context manager for timing request processing"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000
        MetricsService.record_response_time(duration_ms)
        
        # Log to request context if available
        if hasattr(g, "request_id"):
            from flask import current_app
            current_app.logger.info(
                f"Request {g.request_id} completed in {duration_ms:.2f}ms",
                extra={
                    "request_id": g.request_id,
                    "endpoint": self.endpoint,
                    "duration_ms": duration_ms,
                }
            )
        
        return False


# Convenience function
def track_request(endpoint: str):
    """Track request timing"""
    return RequestTimer(endpoint)

