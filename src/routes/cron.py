"""
Cron Jobs for Automated Tasks
Follow-ups, session cleanup, etc.
"""

import os

from flask import Blueprint, jsonify, request

from src.services.followup_automation import followup_automation
from src.services.session_timeout import session_timeout_service

cron_bp = Blueprint("cron", __name__)


def require_cron_key(f):
    """Decorator to require cron API key"""

    def decorated_function(*args, **kwargs):
        cron_key = os.getenv("CRON_API_KEY") or os.getenv("API_KEY")
        if cron_key:
            provided_key = request.headers.get("X-CRON-KEY") or request.headers.get("X-API-KEY")
            if provided_key != cron_key:
                return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function


@cron_bp.route("/health", methods=["GET"])
def cron_health():
    """Health check for cron service"""
    return jsonify({"status": "healthy", "service": "cron"}), 200


@cron_bp.route("/send-followups", methods=["POST"])
@require_cron_key
def send_followups():
    """
    Send automated follow-ups for abandoned conversations
    Should be called daily via cron job

    POST /api/cron/send-followups
    Header: X-CRON-KEY: your_cron_key
    """
    try:
        # Get conversations needing follow-up
        followups = followup_automation.get_conversations_needing_followup()

        sent_count = 0
        failed_count = 0

        for followup in followups:
            success = followup_automation.send_followup(followup)
            if success:
                sent_count += 1
            else:
                failed_count += 1

        return (
            jsonify(
                {
                    "status": "success",
                    "sent": sent_count,
                    "failed": failed_count,
                    "total_checked": len(followups),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@cron_bp.route("/check-secrets", methods=["POST"])
@require_cron_key
def check_secrets():
    """
    Check API keys and secrets for expiration
    Should be called weekly via cron job

    POST /api/cron/check-secrets
    Header: X-CRON-KEY: your_cron_key
    """
    try:
        import subprocess
        import sys

        # Run secret expiration check script
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "scripts",
            "check_secret_expiration.py",
        )

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        return (
            jsonify(
                {
                    "status": "success" if result.returncode == 0 else "warning",
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr if result.stderr else None,
                }
            ),
            200,
        )

    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "error": "Script timeout (>30s)"}), 500
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@cron_bp.route("/cleanup-sessions", methods=["POST"])
@require_cron_key
def cleanup_sessions():
    """
    Clean up old inactive sessions
    Should be called hourly via cron job

    POST /api/cron/cleanup-sessions
    Header: X-CRON-KEY: your_cron_key
    """
    try:
        session_timeout_service.cleanup_old_sessions()

        return jsonify({"status": "success", "message": "Sessions cleaned up"}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@cron_bp.route("/high-value-alerts", methods=["POST"])
@require_cron_key
def high_value_alerts():
    """
    Get alerts for high-value abandoned conversations
    Should be called every 6 hours

    POST /api/cron/high-value-alerts
    Header: X-CRON-KEY: your_cron_key
    """
    try:
        high_value = followup_automation.get_high_value_abandoned()

        # Filter only very high value (>100k PLN estimated)
        critical = [hv for hv in high_value if hv["estimated_value"] > 100000]

        return (
            jsonify(
                {
                    "status": "success",
                    "high_value_count": len(high_value),
                    "critical_count": len(critical),
                    "critical_leads": critical[:10],  # Top 10
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@cron_bp.route("/test", methods=["GET"])
@require_cron_key
def test_cron():
    """
    Test cron functionality without sending actual messages

    GET /api/cron/test
    Header: X-CRON-KEY: your_cron_key
    """
    try:
        # Get followups (but don't send)
        followups = followup_automation.get_conversations_needing_followup()
        high_value = followup_automation.get_high_value_abandoned()

        return (
            jsonify(
                {
                    "status": "success",
                    "followups_ready": len(followups),
                    "high_value_abandoned": len(high_value),
                    "sample_followups": followups[:3] if followups else [],
                    "sample_high_value": high_value[:3] if high_value else [],
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
