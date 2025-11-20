"""
Test refactored chatbot components
Tests state machine, validator, rate limiter, retry logic
"""

from src.services.context_validator import ContextValidator
from src.services.conversation_state_machine import ConversationState, ConversationStateMachine
from src.services.rate_limiter import ConversationRateLimiter, RateLimiter
from src.services.retry_handler import RetryConfig, failed_operations


class TestContextValidator:
    """Test context validation and sanitization"""

    def test_validate_email_valid(self):
        valid, sanitized, error = ContextValidator.validate_email("Test@Example.com")
        assert valid is True
        assert sanitized == "test@example.com"
        assert error is None

    def test_validate_email_invalid(self):
        valid, sanitized, error = ContextValidator.validate_email("invalid-email")
        assert valid is False
        assert error == "Invalid email format"

    def test_validate_phone_polish(self):
        valid, sanitized, error = ContextValidator.validate_phone("123456789")
        assert valid is True
        assert sanitized == "+48123456789"

    def test_validate_phone_with_prefix(self):
        valid, sanitized, error = ContextValidator.validate_phone("+48 123 456 789")
        assert valid is True
        assert sanitized == "+48123456789"

    def test_validate_city_major(self):
        valid, sanitized, error = ContextValidator.validate_city("warszawa")
        assert valid is True
        assert sanitized == "Warszawa"

    def test_validate_square_meters_valid(self):
        valid, sanitized, error = ContextValidator.validate_square_meters("60")
        assert valid is True
        assert sanitized == 60

    def test_validate_square_meters_too_small(self):
        valid, sanitized, error = ContextValidator.validate_square_meters("10")
        assert valid is False
        assert "too small" in error

    def test_validate_package_valid(self):
        valid, sanitized, error = ContextValidator.validate_package("express")
        assert valid is True
        assert sanitized == "Express"

    def test_validate_context_complete(self):
        context = {
            "email": "test@example.com",
            "phone": "123456789",
            "city": "warszawa",
            "square_meters": "60",
            "package": "express",
            "name": "Jan Kowalski",
        }
        valid, sanitized, errors = ContextValidator.validate_context(context)
        assert valid is True
        assert len(errors) == 0
        assert sanitized["email"] == "test@example.com"
        assert sanitized["phone"] == "+48123456789"


class TestConversationStateMachine:
    """Test conversation state machine"""

    def test_initial_state(self):
        sm = ConversationStateMachine()
        assert sm.current_state == ConversationState.GREETING

    def test_valid_transition(self):
        sm = ConversationStateMachine()
        success, error = sm.transition(ConversationState.COLLECTING_INFO)
        assert success is True
        assert error is None
        assert sm.current_state == ConversationState.COLLECTING_INFO

    def test_invalid_transition(self):
        sm = ConversationStateMachine()
        success, error = sm.transition(ConversationState.CONFIRMING)
        assert success is False
        assert "Invalid transition" in error

    def test_determine_state_greeting(self):
        sm = ConversationStateMachine()
        state = sm.determine_state({})
        assert state == ConversationState.GREETING

    def test_determine_state_collecting(self):
        sm = ConversationStateMachine()
        state = sm.determine_state({"package": "Express"})
        assert state == ConversationState.COLLECTING_INFO

    def test_determine_state_qualifying(self):
        sm = ConversationStateMachine()
        state = sm.determine_state({"package": "Express", "name": "Jan"})
        assert state == ConversationState.QUALIFYING

    def test_determine_state_confirming(self):
        sm = ConversationStateMachine()
        state = sm.determine_state(
            {
                "package": "Express",
                "name": "Jan",
                "email": "jan@example.com",
            }
        )
        assert state == ConversationState.CONFIRMING

    def test_should_ask_confirmation_ready(self):
        sm = ConversationStateMachine()
        context = {
            "name": "Jan",
            "email": "jan@example.com",
            "package": "Express",
            "square_meters": "60",
        }
        assert sm.should_ask_confirmation(context) is True

    def test_should_ask_confirmation_not_ready(self):
        sm = ConversationStateMachine()
        context = {"name": "Jan"}
        assert sm.should_ask_confirmation(context) is False

    def test_get_next_required_field(self):
        sm = ConversationStateMachine()
        assert sm.get_next_required_field({}) == "package"
        assert sm.get_next_required_field({"package": "Express"}) == "square_meters"
        assert sm.get_next_required_field({"package": "Express", "square_meters": "60"}) == "city"


class TestRateLimiter:
    """Test rate limiting"""

    def test_rate_limit_allowed(self):
        limiter = RateLimiter()
        allowed, retry_after = limiter.check_rate_limit(
            "test_session", "session", max_requests=5, window_seconds=60
        )
        assert allowed is True
        assert retry_after is None

    def test_rate_limit_exceeded(self):
        limiter = RateLimiter()
        # Make 5 requests
        for i in range(5):
            limiter.check_rate_limit("test_session", "session", max_requests=5, window_seconds=60)

        # 6th request should be denied
        allowed, retry_after = limiter.check_rate_limit(
            "test_session", "session", max_requests=5, window_seconds=60
        )
        assert allowed is False
        assert retry_after is not None

    def test_conversation_spam_detection(self):
        limiter = ConversationRateLimiter()
        # Add duplicate messages
        for i in range(4):
            limiter.add_message("test_session", "spam message")

        is_spam, reason = limiter.is_spam("test_session", "spam message")
        assert is_spam is True
        assert "Duplicate" in reason


class TestRetryLogic:
    """Test retry logic"""

    def test_retry_config(self):
        config = RetryConfig(
            max_attempts=3, initial_delay=1.0, max_delay=10.0, exponential_base=2.0
        )
        assert config.max_attempts == 3
        assert config.initial_delay == 1.0

    def test_failed_operations_queue(self):
        queue = failed_operations
        queue.clear()

        queue.add("monday_lead", {"name": "Test"}, "Connection error")
        assert len(queue.get_pending()) == 1

        queue.clear()
        assert len(queue.get_pending()) == 0
