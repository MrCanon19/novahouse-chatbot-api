"""
Monitoring & Analytics Service

Query performance logging, error tracking, alerts for high-score leads.
"""

import logging
import os
from datetime import datetime, timezone
from typing import Dict

import requests

logger = logging.getLogger(__name__)


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
        """Send Slack alert about high-score lead"""
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

            requests.post(slack_webhook, json=payload, timeout=5)

        except Exception as e:
            logger.error(f"Failed to send lead alert: {e}")

    @staticmethod
    def get_performance_stats() -> Dict:
        """
        Get application performance statistics

        Returns:
            Dict with performance metrics
        """
        # TODO: Collect actual stats from application
        # For now return mock data
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_hours": 72,
            "total_requests": 15432,
            "error_rate_percent": 0.8,
            "avg_response_time_ms": 145,
            "slow_queries_count": 3,
            "active_sessions": 42,
            "database_connection_pool": {
                "size": 3,
                "active": 1,
                "idle": 2,
            },
        }

    @staticmethod
    def get_alert_status() -> Dict:
        """
        Get current alert status

        Returns:
            Dict with active alerts
        """
        # TODO: Implement actual alert collection
        # For now return mock data
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_alerts": [
                {
                    "type": "high_score_lead",
                    "severity": "critical",
                    "message": "5 leads with score >= 80 waiting for contact",
                    "count": 5,
                },
                {
                    "type": "sla_breach",
                    "severity": "high",
                    "message": "2 leads with breached SLA",
                    "count": 2,
                },
                {
                    "type": "slow_query",
                    "severity": "medium",
                    "message": "1 slow query detected (> 500ms)",
                    "count": 1,
                },
            ],
            "total_active_alerts": 8,
        }


# Singleton instance
monitoring_service = MonitoringService()
