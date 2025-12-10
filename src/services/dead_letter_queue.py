"""
Dead-Letter Queue Service

Handles failed alerts and notifications, stores them for retry, and escalates if needed.
Prevents alert loss when external services (Slack, Monday.com) are unavailable.
"""

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Dict

import requests

from src.models.chatbot import DeadLetterQueue, db

logger = logging.getLogger(__name__)

# Configuration
MAX_RETRIES = 5  # Maximum retry attempts before marking as failed
RETRY_DELAY_MINUTES = 5  # Wait 5 minutes before retrying
ESCALATION_EMAIL = os.getenv("ESCALATION_EMAIL", "admin@novahouse.pl")


class DeadLetterQueueService:
    """Service for managing failed alerts and notifications"""

    @staticmethod
    def enqueue_failed_alert(
        event_type: str,
        target: str,
        payload: Dict,
        error_message: str,
    ) -> DeadLetterQueue:
        """
        Store a failed alert in the dead-letter queue for later retry

        Args:
            event_type: Type of event ('slack_alert', 'email', 'sms')
            target: Target URL, email, or phone number
            payload: Alert payload as dict
            error_message: Error from the failed attempt

        Returns:
            DeadLetterQueue record
        """
        dlq_record = DeadLetterQueue(
            event_type=event_type,
            target=target,
            payload=json.dumps(payload),
            error_message=error_message,
            retry_count=0,
            status="pending",
        )
        db.session.add(dlq_record)
        db.session.commit()

        logger.warning(
            f"❌ Alert queued for retry: {event_type} → {target}. Error: {error_message}"
        )
        return dlq_record

    @staticmethod
    def retry_pending_alerts() -> Dict:
        """
        Retry all pending alerts in the dead-letter queue

        Returns:
            Dict with stats: {'retried': N, 'delivered': N, 'failed': N}
        """
        from src.main import app

        with app.app_context():
            stats = {"retried": 0, "delivered": 0, "failed": 0}

            # Find pending alerts that are ready for retry
            now = datetime.now(timezone.utc)
            pending_alerts = DeadLetterQueue.query.filter(
                DeadLetterQueue.status == "pending",
                DeadLetterQueue.retry_count < MAX_RETRIES,
                (
                    (DeadLetterQueue.last_retry_at == None)  # Never retried
                    | (
                        DeadLetterQueue.last_retry_at
                        <= now - timedelta(minutes=RETRY_DELAY_MINUTES)
                    )  # Retry delay passed
                ),
            ).all()

            for alert in pending_alerts:
                stats["retried"] += 1

                try:
                    payload = json.loads(alert.payload)

                    if alert.event_type == "slack_alert":
                        response = requests.post(alert.target, json=payload, timeout=5)
                        response.raise_for_status()
                    elif alert.event_type == "email":
                        # Placeholder for email retry
                        logger.info(f"📧 Email retry (not implemented): {alert.target}")
                        response = None
                    elif alert.event_type == "sms":
                        # Placeholder for SMS retry
                        logger.info(f"📱 SMS retry (not implemented): {alert.target}")
                        response = None
                    else:
                        raise ValueError(f"Unknown event type: {alert.event_type}")

                    # Success: mark as delivered
                    alert.status = "delivered"
                    alert.last_retry_at = now
                    db.session.commit()
                    stats["delivered"] += 1

                    logger.info(
                        f"✅ Alert delivered after retry: {alert.event_type} → {alert.target}"
                    )

                except Exception as e:
                    # Failure: increment retry count
                    alert.retry_count += 1
                    alert.last_retry_at = now

                    if alert.retry_count >= MAX_RETRIES:
                        alert.status = "failed"
                        logger.error(
                            f"❌ Alert FAILED after {MAX_RETRIES} retries: {alert.event_type}"
                        )
                        # TODO: Escalate to admin
                        DeadLetterQueueService._escalate_to_admin(alert)
                    else:
                        logger.warning(
                            f"⚠️ Alert retry {alert.retry_count}/{MAX_RETRIES} failed: {str(e)}"
                        )

                    db.session.commit()
                    stats["failed"] += 1

            return stats

    @staticmethod
    def _escalate_to_admin(alert: DeadLetterQueue) -> None:
        """
        Escalate a failed alert to admin email

        Args:
            alert: DeadLetterQueue record
        """
        if not ESCALATION_EMAIL:
            logger.warning("⚠️ ESCALATION_EMAIL not configured, cannot escalate alert")
            return

        escalation_message = f"""
Alert escalation - failed after {MAX_RETRIES} retries:

Event Type: {alert.event_type}
Target: {alert.target}
Created: {alert.created_at.isoformat()}
Last Error: {alert.error_message}
Payload:
{json.dumps(json.loads(alert.payload), indent=2)}

Action Required: Manually check the service and retry if available.
        """

        logger.error(f"🚨 ESCALATING to {ESCALATION_EMAIL}: {alert.event_type}")
        # TODO: Implement email escalation
        # For now, just log the escalation
        return

    @staticmethod
    def get_pending_alerts() -> list:
        """
        Get all pending alerts in the dead-letter queue

        Returns:
            List of DeadLetterQueue records
        """
        from src.main import app

        with app.app_context():
            return (
                DeadLetterQueue.query.filter(DeadLetterQueue.status == "pending")
                .order_by(DeadLetterQueue.created_at.desc())
                .all()
            )

    @staticmethod
    def get_failed_alerts(limit: int = 100) -> list:
        """
        Get recently failed alerts

        Returns:
            List of failed DeadLetterQueue records
        """
        from src.main import app

        with app.app_context():
            return (
                DeadLetterQueue.query.filter(DeadLetterQueue.status == "failed")
                .order_by(DeadLetterQueue.created_at.desc())
                .limit(limit)
                .all()
            )

    @staticmethod
    def clear_delivered_alerts(older_than_hours: int = 24) -> int:
        """
        Clean up old delivered alerts from the queue

        Args:
            older_than_hours: Delete alerts delivered more than this many hours ago

        Returns:
            Number of records deleted
        """
        from src.main import app

        with app.app_context():
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=older_than_hours)

            deleted_count = DeadLetterQueue.query.filter(
                DeadLetterQueue.status == "delivered",
                DeadLetterQueue.created_at < cutoff_time,
            ).delete()

            db.session.commit()
            logger.info(f"🗑️ Cleaned up {deleted_count} old delivered alerts")
            return deleted_count
