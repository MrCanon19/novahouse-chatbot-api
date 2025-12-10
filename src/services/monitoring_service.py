"""
Monitoring & Analytics Service

Query performance logging, error tracking, alerts for high-score leads.
"""

import logging
import os
from datetime import datetime, timezone
from typing import Dict

import requests
from pybreaker import CircuitBreaker

logger = logging.getLogger(__name__)

# Circuit breakers for external APIs (fail-fast on repeated failures)
slack_breaker = CircuitBreaker(
    fail_max=5,  # Open after 5 failures
    reset_timeout=60,  # Wait 60 seconds before attempting recovery
    listeners=[],  # Could add listeners for alerting on state changes
)
logger.info("✅ Slack circuit breaker initialized (fail_max=5, reset_timeout=60s)")


class MonitoringService:
    """Service for application monitoring and analytics"""

    # Alert thresholds
    HIGH_SCORE_LEAD_THRESHOLD = 80  # Alert when lead score >= 80
    SLOW_QUERY_THRESHOLD_MS = 100  # Alert for queries > 100ms
    ERROR_RATE_THRESHOLD = 5  # Alert if error rate > 5%

    @staticmethod
    def log_query_performance(
        query_name: str,
        duration_ms: float,
        table: str = None,
        row_count: int = None,
    ) -> None:
        """
        Log database query performance

        Args:
            query_name: Name/description of query
            duration_ms: Execution time in milliseconds
            table: Table name (optional)
            row_count: Number of rows affected (optional)
        """
        if duration_ms > MonitoringService.SLOW_QUERY_THRESHOLD_MS:
            logger.warning(
                f"⚠️  Slow query: {query_name} ({duration_ms:.2f}ms)"
                + (f" on {table}" if table else "")
                + (f" - {row_count} rows" if row_count else "")
            )

            # Send alert if very slow
            if duration_ms > 500:
                MonitoringService._alert_slow_query(query_name, duration_ms, table, row_count)
        else:
            logger.debug(
                f"✓ Query: {query_name} ({duration_ms:.2f}ms)"
                + (f" - {row_count} rows" if row_count else "")
            )

    @staticmethod
    def log_api_call(
        endpoint: str,
        method: str,
        status_code: int,
        duration_ms: float,
    ) -> None:
        """
        Log API call performance

        Args:
            endpoint: API endpoint
            method: HTTP method (GET, POST, etc.)
            status_code: HTTP status code
            duration_ms: Request duration in milliseconds
        """
        if status_code >= 400:
            logger.warning(
                f"❌ API Error: {method} {endpoint} - {status_code} ({duration_ms:.2f}ms)"
            )
        elif duration_ms > 500:
            logger.warning(f"⚠️  Slow API: {method} {endpoint} - {duration_ms:.2f}ms")
        else:
            logger.info(f"✓ {method} {endpoint} - {status_code} ({duration_ms:.2f}ms)")

    @staticmethod
    def alert_high_score_lead(lead_id: int, score: int, lead_info: Dict) -> None:
        """
        Alert about high-score lead (likely ready to convert)

        Args:
            lead_id: Lead ID
            score: Lead score (0-100)
            lead_info: Lead information
        """
        if score < MonitoringService.HIGH_SCORE_LEAD_THRESHOLD:
            return

        logger.info(f"🔴 HIGH-SCORE LEAD ALERT: Lead {lead_id} - Score: {score}/100")

        # Send Slack alert
        MonitoringService._send_lead_alert(lead_id, score, lead_info)

    @staticmethod
    def _alert_slow_query(
        query_name: str,
        duration_ms: float,
        table: str = None,
        row_count: int = None,
    ) -> None:
        """Send alert about slow query"""
        try:
            slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
            if not slack_webhook:
                return

            payload = {
                "text": "⚠️  Slow Database Query Alert",
                "attachments": [
                    {
                        "color": "#FFA500",
                        "fields": [
                            {"title": "Query", "value": query_name, "short": True},
                            {
                                "title": "Duration",
                                "value": f"{duration_ms:.2f}ms",
                                "short": True,
                            },
                            {"title": "Table", "value": table or "N/A", "short": True},
                            {
                                "title": "Rows",
                                "value": str(row_count or "N/A"),
                                "short": True,
                            },
                            {
                                "title": "Timestamp",
                                "value": datetime.now(timezone.utc).isoformat(),
                                "short": False,
                            },
                        ],
                    }
                ],
            }

            requests.post(slack_webhook, json=payload, timeout=5)

        except Exception as e:
            logger.error(f"Failed to send slow query alert: {e}")

    @staticmethod
    def _send_lead_alert(lead_id: int, score: int, lead_info: Dict) -> None:
        """
        Send Slack alert about high-score lead (WITH CIRCUIT BREAKER + DEAD-LETTER QUEUE)

        Circuit breaker opens after 5 consecutive failures, preventing cascading
        failures and thundering herd problem when Slack API is down.

        Failed alerts are stored in dead-letter queue for retry when Slack recovers.
        """
        try:
            slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
            if not slack_webhook:
                return

            payload = {
                "text": "🔴 HIGH-SCORE LEAD - READY TO CONVERT",
                "attachments": [
                    {
                        "color": "#FF0000",
                        "fields": [
                            {"title": "Lead ID", "value": str(lead_id), "short": True},
                            {"title": "Score", "value": f"{score}/100", "short": True},
                            {
                                "title": "Name",
                                "value": lead_info.get("name", "N/A"),
                                "short": True,
                            },
                            {
                                "title": "Email",
                                "value": lead_info.get("email", "N/A"),
                                "short": True,
                            },
                            {
                                "title": "Phone",
                                "value": lead_info.get("phone", "N/A"),
                                "short": True,
                            },
                            {
                                "title": "Package",
                                "value": lead_info.get("package", "N/A"),
                                "short": True,
                            },
                            {
                                "title": "Action",
                                "value": "⚡ CALL IMMEDIATELY",
                                "short": False,
                            },
                        ],
                    }
                ],
            }

            # Circuit breaker protects against cascading failures when Slack is down
            @slack_breaker
            def send_slack():
                requests.post(slack_webhook, json=payload, timeout=5)

            send_slack()
            logger.info(f"✅ Slack alert sent for lead {lead_id}")

        except Exception as e:
            # Import here to avoid circular import
            from src.services.dead_letter_queue import DeadLetterQueueService

            logger.warning(f"⚠️  Failed to send lead alert: {e} (circuit breaker may be open)")

            # Store in dead-letter queue for retry
            try:
                slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
                if slack_webhook:
                    DeadLetterQueueService.enqueue_failed_alert(
                        event_type="slack_alert",
                        target=slack_webhook,
                        payload=payload,
                        error_message=str(e),
                    )
            except Exception as dlq_error:
                logger.error(f"❌ Failed to enqueue alert in DLQ: {dlq_error}")

    @staticmethod
    def get_performance_stats() -> Dict:
        """
        Get application performance statistics

        Returns:
            Dict with performance metrics
        """
        from src.main import db
        from src.services.redis_service import get_redis_cache

        stats = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Redis/Cache stats
        try:
            cache = get_redis_cache()
            cache_stats = cache.get_stats()
            stats["cache"] = cache_stats
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            stats["cache"] = {"error": str(e)}

        # Database connection pool stats
        try:
            if hasattr(db.engine.pool, "size"):
                pool = db.engine.pool
                stats["database_connection_pool"] = {
                    "size": pool.size(),
                    "checked_in": pool.checkedin(),
                    "checked_out": pool.checkedout(),
                    "overflow": pool.overflow(),
                }
        except Exception as e:
            logger.error(f"Failed to get DB pool stats: {e}")
            stats["database_connection_pool"] = {"error": str(e)}

        return stats

    @staticmethod
    def get_alert_status() -> Dict:
        """
        Get current alert status

        Returns:
            Dict with active alerts
        """
        from src.main import db
        from src.models.chatbot import Lead

        active_alerts = []

        try:
            # High-score leads waiting for contact
            high_score_leads = (
                db.session.query(Lead)
                .filter(
                    Lead.score >= MonitoringService.HIGH_SCORE_LEAD_THRESHOLD,
                    Lead.status.in_(["new", "contacted"]),
                )
                .count()
            )

            if high_score_leads > 0:
                active_alerts.append(
                    {
                        "type": "high_score_lead",
                        "severity": "critical",
                        "message": f"{high_score_leads} leads with score >= {MonitoringService.HIGH_SCORE_LEAD_THRESHOLD} waiting for contact",
                        "count": high_score_leads,
                    }
                )

            # New leads requiring action (not contacted in 24h)
            from datetime import timedelta

            threshold_time = datetime.now(timezone.utc) - timedelta(hours=24)
            stale_leads = (
                db.session.query(Lead)
                .filter(Lead.status == "new", Lead.created_at < threshold_time)
                .count()
            )

            if stale_leads > 0:
                active_alerts.append(
                    {
                        "type": "stale_leads",
                        "severity": "high",
                        "message": f"{stale_leads} new leads not contacted in 24h",
                        "count": stale_leads,
                    }
                )

        except Exception as e:
            logger.error(f"Failed to get alert status: {e}")
            active_alerts.append(
                {
                    "type": "monitoring_error",
                    "severity": "medium",
                    "message": f"Failed to query alerts: {str(e)}",
                    "count": 0,
                }
            )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_alerts": active_alerts,
            "total_active_alerts": len(active_alerts),
        }


# Singleton instance
monitoring_service = MonitoringService()
