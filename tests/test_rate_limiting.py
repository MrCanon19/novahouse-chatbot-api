"""Tests for rate limiting configuration and DummyLimiter."""
import os
import pytest


class TestRateLimitingHelpers:
    """Test rate limiting helper functions and classes."""

    def test_is_rate_limit_disabled_when_set_to_false(self):
        """Test that is_rate_limit_disabled returns True when env var is 'false'."""
        # Set env var and reimport to test
        os.environ["RATE_LIMIT_ENABLED"] = "false"
        from src.middleware.rate_limiting import is_rate_limit_disabled
        assert is_rate_limit_disabled() is True

    def test_is_rate_limit_disabled_when_set_to_true(self):
        """Test that is_rate_limit_disabled returns False when env var is 'true'."""
        os.environ["RATE_LIMIT_ENABLED"] = "true"
        from src.middleware.rate_limiting import is_rate_limit_disabled
        assert is_rate_limit_disabled() is False

    def test_is_rate_limit_disabled_default(self):
        """Test that is_rate_limit_disabled defaults to False when not set."""
        # Remove env var if it exists
        os.environ.pop("RATE_LIMIT_ENABLED", None)
        from src.middleware.rate_limiting import is_rate_limit_disabled
        assert is_rate_limit_disabled() is False

    def test_is_rate_limit_disabled_case_insensitive(self):
        """Test that is_rate_limit_disabled is case insensitive."""
        os.environ["RATE_LIMIT_ENABLED"] = "FALSE"
        from src.middleware.rate_limiting import is_rate_limit_disabled
        assert is_rate_limit_disabled() is True

        os.environ["RATE_LIMIT_ENABLED"] = "FALSE"
        from src.middleware.rate_limiting import is_rate_limit_disabled
        assert is_rate_limit_disabled() is True


class TestDummyLimiter:
    """Test DummyLimiter class for no-op rate limiting."""

    def test_dummy_limiter_returns_decorator(self):
        """Test that DummyLimiter.limit() returns a decorator."""
        from src.middleware.rate_limiting import DummyLimiter

        limiter = DummyLimiter()
        decorator = limiter.limit()

        # Decorator should be callable
        assert callable(decorator)

    def test_dummy_limiter_decorator_returns_function(self):
        """Test that DummyLimiter decorator returns the function unchanged."""
        from src.middleware.rate_limiting import DummyLimiter

        limiter = DummyLimiter()
        decorator = limiter.limit()

        def test_func():
            return "test_value"

        wrapped = decorator(test_func)

        # Should return the original function unchanged
        assert wrapped is test_func
        assert wrapped() == "test_value"

    def test_dummy_limiter_with_args(self):
        """Test that DummyLimiter.limit() works with arguments."""
        from src.middleware.rate_limiting import DummyLimiter

        limiter = DummyLimiter()
        # Should accept any arguments and return decorator
        decorator = limiter.limit("10 per minute")

        assert callable(decorator)

        def test_func():
            return "result"

        wrapped = decorator(test_func)
        assert wrapped() == "result"

    def test_dummy_limiter_with_kwargs(self):
        """Test that DummyLimiter.limit() works with keyword arguments."""
        from src.middleware.rate_limiting import DummyLimiter

        limiter = DummyLimiter()
        # Should accept any keyword arguments
        decorator = limiter.limit("10 per minute", key_func=lambda: "test")

        assert callable(decorator)

        def test_func():
            return "result"

        wrapped = decorator(test_func)
        assert wrapped() == "result"


class TestRateLimitingIntegration:
    """Integration tests for rate limiting in Flask app."""

    def test_api_endpoint_works_without_rate_limiting(self, app):
        """Test that API endpoints work when rate limiting is disabled."""
        with app.test_client() as client:
            # Health endpoint should work multiple times rapidly
            for _ in range(5):
                response = client.get("/api/health")
                assert response.status_code == 200  # Should always be 200 with DummyLimiter



class TestRateLimitingEnvironmentVariables:
    """Test environment variable configuration for rate limiting."""

    def test_rate_limit_enabled_env_var_default(self):
        """Test RATE_LIMIT_ENABLED default value."""
        # When not set, should default to "true"
        os.environ.pop("RATE_LIMIT_ENABLED", None)
        from src.middleware.rate_limiting import is_rate_limit_disabled

        # Default should be False (meaning rate limiting IS enabled)
        assert is_rate_limit_disabled() is False

    def test_rate_limit_enabled_env_var_true_value(self):
        """Test RATE_LIMIT_ENABLED=true enables rate limiting."""
        os.environ["RATE_LIMIT_ENABLED"] = "true"
        from src.middleware.rate_limiting import is_rate_limit_disabled

        assert is_rate_limit_disabled() is False

    def test_rate_limit_enabled_env_var_false_value(self):
        """Test RATE_LIMIT_ENABLED=false disables rate limiting."""
        os.environ["RATE_LIMIT_ENABLED"] = "false"
        from src.middleware.rate_limiting import is_rate_limit_disabled

        assert is_rate_limit_disabled() is True
