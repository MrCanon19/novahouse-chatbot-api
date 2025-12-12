"""
Retry Logic for External Integrations
Handles transient failures with exponential backoff
"""

import time
from functools import wraps
from typing import Any, Callable, Optional, Tuple


class RetryConfig:
    """Retry configuration"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 10.0,
        exponential_base: float = 2.0,
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base


def retry_with_backoff(
    config: Optional[RetryConfig] = None,
    exceptions: Tuple[type, ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None,
):
    """
    Decorator for retrying functions with exponential backoff

    Args:
        config: Retry configuration
        exceptions: Tuple of exception types to retry on
        on_retry: Callback function called on each retry (attempt_number, exception)

    Example:
        @retry_with_backoff(
            config=RetryConfig(max_attempts=3),
            exceptions=(ConnectionError, TimeoutError)
        )
        def call_external_api():
            ...
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            delay = config.initial_delay

            while attempt < config.max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1

                    # Last attempt, raise the exception
                    if attempt >= config.max_attempts:
                        print(f"[Retry] {func.__name__} failed after {attempt} attempts: {e}")
                        raise

                    # Call retry callback if provided
                    if on_retry:
                        on_retry(attempt, e)

                    print(
                        f"[Retry] {func.__name__} attempt {attempt}/{config.max_attempts} failed: {e}. Retrying in {delay}s..."
                    )

                    # Wait before retry
                    time.sleep(delay)

                    # Exponential backoff
                    delay = min(delay * config.exponential_base, config.max_delay)

            # Should never reach here
            raise RuntimeError(f"Retry logic failed for {func.__name__}")

        return wrapper

    return decorator


class FailedOperationQueue:
    """
    Queue for failed operations that need to be retried later
    Simple in-memory queue (could be replaced with Redis/RabbitMQ for production)
    """

    def __init__(self):
        self.queue = []

    def add(self, operation_type: str, operation_data: dict, error: str):
        """Add failed operation to queue"""
        self.queue.append(
            {
                "type": operation_type,
                "data": operation_data,
                "error": error,
                "attempts": 0,
                "timestamp": time.time(),
            }
        )
        print(f"[FailedQueue] Added {operation_type}: {error}")

    def get_pending(self, operation_type: Optional[str] = None) -> list:
        """Get pending operations, optionally filtered by type"""
        if operation_type:
            return [op for op in self.queue if op["type"] == operation_type]
        return self.queue

    def remove(self, operation):
        """Remove operation from queue"""
        if operation in self.queue:
            self.queue.remove(operation)

    def retry_all(self, max_attempts: int = 3):
        """
        Retry all pending operations

        Returns:
            (success_count, failed_count)
        """
        success = 0
        failed = 0

        for operation in list(self.queue):  # Copy to avoid modification during iteration
            operation["attempts"] += 1

            if operation["attempts"] > max_attempts:
                print(f"[FailedQueue] Abandoning {operation['type']} after {max_attempts} attempts")
                self.remove(operation)
                failed += 1
                continue

            try:
                # Retry based on type
                if operation["type"] == "monday_lead":
                    from src.integrations.monday_client import MondayClient

                    monday = MondayClient()
                    monday.create_lead_item(operation["data"])
                    print("[FailedQueue] Successfully retried monday_lead")
                    self.remove(operation)
                    success += 1

                elif operation["type"] == "email":
                    from src.services.email_service import email_service

                    email_service.send_email(**operation["data"])
                    print("[FailedQueue] Successfully retried email")
                    self.remove(operation)
                    success += 1

                else:
                    print(f"[FailedQueue] Unknown operation type: {operation['type']}")
                    failed += 1

            except Exception as e:
                print(f"[FailedQueue] Retry failed for {operation['type']}: {e}")
                failed += 1

        return success, failed

    def clear(self):
        """Clear all pending operations"""
        count = len(self.queue)
        self.queue.clear()
        print(f"[FailedQueue] Cleared {count} operations")
        return count


# Global instance
failed_operations = FailedOperationQueue()


# Pre-configured retry decorators for common integrations
def retry_monday_api(func: Callable) -> Callable:
    """Retry decorator for Monday.com API calls"""
    return retry_with_backoff(
        config=RetryConfig(max_attempts=3, initial_delay=2.0),
        exceptions=(ConnectionError, TimeoutError, Exception),
        on_retry=lambda attempt, error: logging.warning(f"[Monday] Retry {attempt}/3 due to: {error}"),
    )(func)


def retry_openai_api(func: Callable) -> Callable:
    """Retry decorator for OpenAI API calls"""
    return retry_with_backoff(
        config=RetryConfig(max_attempts=2, initial_delay=1.0),
        exceptions=(ConnectionError, TimeoutError),
        on_retry=lambda attempt, error: logging.warning(f"[OpenAI] Retry {attempt}/2 due to: {error}"),
    )(func)


def retry_email_send(func: Callable) -> Callable:
    """Retry decorator for email sending"""
    return retry_with_backoff(
        config=RetryConfig(max_attempts=3, initial_delay=1.5),
        exceptions=(ConnectionError, TimeoutError, Exception),
        on_retry=lambda attempt, error: logging.warning(f"[Email] Retry {attempt}/3 due to: {error}"),
    )(func)
