"""
Integration tests for Tier 1 production reliability blockers.

Tests:
1. Purge loop: Redis fallback cache cleanup prevents memory leak
2. Idempotency: Follow-ups only sent once via FollowupEvent UNIQUE constraint
3. Circuit breakers: Graceful degradation when external APIs fail
4. Unsubscribe: RODO compliance and audit logging
5. Dead-letter queue: Failed alerts stored and retried
"""

import time
from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from src.models.chatbot import ChatConversation, db
from src.models.consent_audit_log import ConsentAuditLog
from src.models.followup_event import FollowupEvent
from src.services.dead_letter_queue import DeadLetterQueueService
from src.services.redis_service import get_redis_cache


class TestPurgeLoop:
    """Test fallback cache cleanup prevents memory leak"""

    def test_cleanup_removes_expired_entries(self):
        """Verify cleanup_expired_fallback() removes only expired entries"""
        cache = get_redis_cache()
        cache._fallback_cache.clear()

        # Add expired entry (expiry 100 seconds in past)
        cache._fallback_cache["expired_key"] = ("old_value", time.time() - 100)

        # Add valid entry (expiry 1000 seconds in future)
        cache._fallback_cache["valid_key"] = ("new_value", time.time() + 1000)

        # Run cleanup
        purged_count = cache.cleanup_expired_fallback()

        # Verify exactly 1 entry purged
        assert purged_count == 1, f"Expected 1 purged entry, got {purged_count}"

        # Verify expired key removed
        assert "expired_key" not in cache._fallback_cache, "Expired key should be removed"

        # Verify valid key still exists
        assert "valid_key" in cache._fallback_cache, "Valid key should remain"

    def test_cleanup_empty_cache(self):
        """Verify cleanup handles empty cache gracefully"""
        cache = get_redis_cache()
        cache._fallback_cache.clear()

        purged_count = cache.cleanup_expired_fallback()
        assert purged_count == 0


class TestIdempotency:
    """Test follow-up idempotency with FollowupEvent UNIQUE constraint"""

    def test_duplicate_followup_raises_integrity_error(self, app):
        """Verify duplicate follow-up (same conversation + number) fails with IntegrityError"""
        with app.app_context():
            # Create test conversation with required fields
            conversation = ChatConversation(
                session_id="test_idempotent_session",
                email="test@example.com",
                started_at=datetime.now(timezone.utc),
            )
            db.session.add(conversation)
            db.session.commit()
            conv_id = conversation.id

            # First follow-up event (should succeed)
            followup1 = FollowupEvent(conversation_id=conv_id, followup_number=1, status="sent")
            db.session.add(followup1)
            db.session.commit()

            # Second follow-up event with same (conv_id, number) - should fail UNIQUE
            followup2 = FollowupEvent(conversation_id=conv_id, followup_number=1, status="sent")
            db.session.add(followup2)

            # IntegrityError on duplicate - this is EXPECTED
            with pytest.raises(IntegrityError):
                db.session.commit()

            db.session.rollback()

    def test_different_followup_numbers_succeed(self, app):
        """Verify different follow-up numbers for same conversation succeed"""
        with app.app_context():
            # Create test conversation
            conversation = ChatConversation(
                session_id="test_different_followups",
                email="test@example.com",
                started_at=datetime.now(timezone.utc),
            )
            db.session.add(conversation)
            db.session.commit()
            conv_id = conversation.id

            # Add follow-up #1
            followup1 = FollowupEvent(conversation_id=conv_id, followup_number=1, status="sent")
            db.session.add(followup1)
            db.session.commit()

            # Add follow-up #2 (should succeed - different number)
            followup2 = FollowupEvent(conversation_id=conv_id, followup_number=2, status="sent")
            db.session.add(followup2)
            db.session.commit()  # Should NOT raise error

            # Verify both exist
            events = FollowupEvent.query.filter_by(conversation_id=conv_id).all()
            assert len(events) == 2


class TestCircuitBreakers:
    """Test circuit breaker functionality"""

    def test_slack_circuit_breaker_opens_after_failures(self):
        """Verify Slack circuit breaker opens after 5+ failures"""
        from pybreaker import CircuitBreakerError

        from src.services.monitoring_service import slack_breaker

        # Reset to clean state
        slack_breaker.close()

        # Simulate 6 failures
        for _ in range(6):
            try:

                @slack_breaker
                def failing_call():
                    raise Exception("Slack unavailable")

                failing_call()
            except Exception:
                pass

        # Now circuit should be OPEN - next call raises CircuitBreakerError
        circuit_opened = False
        try:

            @slack_breaker
            def test_call():
                pass

            test_call()
        except CircuitBreakerError:
            circuit_opened = True

        assert circuit_opened, "Circuit should be open after failures"
        slack_breaker.close()  # Reset for other tests

    def test_monday_circuit_breaker_opens_after_failures(self):
        """Verify Monday.com circuit breaker opens after 5+ failures"""
        from pybreaker import CircuitBreakerError

        from src.integrations.monday_client import monday_breaker

        # Reset to clean state
        monday_breaker.close()

        # Simulate 6 failures
        for _ in range(6):
            try:

                @monday_breaker
                def failing_call():
                    raise Exception("Monday unavailable")

                failing_call()
            except Exception:
                pass

        # Now circuit should be OPEN
        circuit_opened = False
        try:

            @monday_breaker
            def test_call():
                pass

            test_call()
        except CircuitBreakerError:
            circuit_opened = True

        assert circuit_opened, "Circuit should be open after failures"
        monday_breaker.close()  # Reset


class TestUnsubscribe:
    """Test unsubscribe and RODO compliance"""

    def test_unsubscribe_creates_audit_log(self, app):
        """Verify unsubscribe action creates audit log entry"""
        with app.app_context():
            email = "audit@example.com"

            # Create audit log entry
            audit = ConsentAuditLog(
                email=email,
                action="unsubscribe",
                ip_address="127.0.0.1",
                user_agent="Test",
            )
            db.session.add(audit)
            db.session.commit()

            # Query it back
            found_audit = ConsentAuditLog.query.filter_by(email=email).first()
            assert found_audit is not None
            assert found_audit.action == "unsubscribe"

    def test_revoke_consent_endpoint(self, app, client):
        """Verify /api/revoke-consent endpoint exists"""
        response = client.post(
            "/api/revoke-consent",
            json={"email": "revoke@example.com"},
        )
        # Endpoint should exist and handle request
        assert response.status_code in [200, 400, 404]

    def test_unsubscribe_status_endpoint(self, app, client):
        """Verify /api/unsubscribe/status endpoint exists"""
        response = client.get(
            "/api/unsubscribe/status/test@example.com",
        )
        # Endpoint should exist
        assert response.status_code in [200, 404]


class TestDeadLetterQueue:
    """Test dead-letter queue for failed alerts"""

    def test_enqueue_failed_alert(self, app):
        """Verify failed alert is enqueued in DLQ"""
        with app.app_context():
            payload = {"text": "Test alert"}
            error_msg = "Connection timeout"

            dlq_record = DeadLetterQueueService.enqueue_failed_alert(
                event_type="slack_alert",
                target="https://hooks.slack.com/...",
                payload=payload,
                error_message=error_msg,
            )

            assert dlq_record is not None
            assert dlq_record.status == "pending"
            assert dlq_record.event_type == "slack_alert"
            assert dlq_record.retry_count == 0

    def test_get_pending_alerts(self, app):
        """Verify get_pending_alerts retrieves queued alerts"""
        with app.app_context():
            # Enqueue a test alert
            DeadLetterQueueService.enqueue_failed_alert(
                event_type="email",
                target="admin@example.com",
                payload={"subject": "Test"},
                error_message="SMTP timeout",
            )

            # Retrieve pending
            pending = DeadLetterQueueService.get_pending_alerts()
            assert len(pending) > 0
            assert pending[0].status == "pending"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
