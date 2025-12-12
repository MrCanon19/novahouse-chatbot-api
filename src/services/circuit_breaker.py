"""
Circuit Breaker for OpenAI API
Prevents cascading failures by stopping requests when API is failing
"""

import logging
import time
from enum import Enum
from typing import Callable, Optional


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for OpenAI API
    
    Prevents making requests when API is failing repeatedly.
    After failure threshold, circuit opens and rejects requests.
    After timeout, circuit goes to half-open to test recovery.
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: type = Exception,
    ):
        """
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before trying again (half-open)
            expected_exception: Exception type that counts as failure
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        # Convert single exception to tuple if needed
        if isinstance(expected_exception, type):
            self.expected_exception = (expected_exception,)
        else:
            self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        self.success_count = 0  # For half-open state
        
    def call(self, func: Callable, *args, **kwargs):
        """
        Execute function with circuit breaker protection
        
        Args:
            func: Function to call
            *args, **kwargs: Arguments to pass to function
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerOpenError: If circuit is open
            Original exception: If function fails
        """
        # Check circuit state
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self.last_failure_time and (time.time() - self.last_failure_time) >= self.recovery_timeout:
                logging.info("[CircuitBreaker] Recovery timeout passed, moving to HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker is OPEN. Last failure: {self.last_failure_time}. "
                    f"Will retry after {self.recovery_timeout}s"
                )
        
        # Try to execute function
        try:
            result = func(*args, **kwargs)
            
            # Success - reset failure count
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= 2:  # Need 2 successes to close
                    logging.info("[CircuitBreaker] Service recovered, closing circuit")
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            else:
                # Reset on success
                self.failure_count = 0
                if self.state == CircuitState.OPEN:
                    self.state = CircuitState.CLOSED
            
            return result
            
        except self.expected_exception as e:
            # Failure - increment count
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            logging.warning(
                f"[CircuitBreaker] Failure {self.failure_count}/{self.failure_threshold}: {type(e).__name__}"
            )
            
            # Open circuit if threshold reached
            if self.failure_count >= self.failure_threshold:
                logging.error(
                    f"[CircuitBreaker] Failure threshold reached ({self.failure_threshold}), opening circuit"
                )
                self.state = CircuitState.OPEN
            
            # Re-raise exception
            raise
    
    def reset(self):
        """Manually reset circuit breaker"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        logging.info("[CircuitBreaker] Manually reset")


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open and rejecting requests"""
    pass


# Global circuit breaker instance for OpenAI API
_openai_circuit_breaker = CircuitBreaker(
    failure_threshold=5,  # Open after 5 failures
    recovery_timeout=60.0,  # Try again after 60 seconds
    expected_exception=Exception,  # Catch all exceptions
)


def get_openai_circuit_breaker() -> CircuitBreaker:
    """Get global OpenAI circuit breaker instance"""
    return _openai_circuit_breaker

