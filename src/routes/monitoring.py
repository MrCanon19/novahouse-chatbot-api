"""
Monitoring & Health Routes

Endpoints for application monitoring, alerts, and diagnostics.
"""

from flask import Blueprint, jsonify

from src.services.monitoring_service import monitoring_service

monitoring_bp = Blueprint("monitoring", __name__, url_prefix="/api/monitoring")


@monitoring_bp.route("/health", methods=["GET"])
def health_check():
    """Detailed health check with stats"""
    try:
        stats = monitoring_service.get_performance_stats()

        # Determine overall health status
        if stats["error_rate_percent"] > 5:
            status = "degraded"
            color = "🟠"
        elif stats["error_rate_percent"] > 2:
            status = "good"
            color = "🟢"
        else:
            status = "excellent"
            color = "✅"

        return (
            jsonify(
                {
                    "status": status,
                    "indicator": color,
                    "stats": stats,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500


@monitoring_bp.route("/alerts", methods=["GET"])
def get_alerts():
    """Get active alerts"""
    try:
        alerts = monitoring_service.get_alert_status()
        return jsonify(alerts), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@monitoring_bp.route("/performance", methods=["GET"])
def get_performance():
    """Get performance statistics"""
    try:
        stats = monitoring_service.get_performance_stats()
        return jsonify(stats), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@monitoring_bp.route("/status", methods=["GET"])
def status():
    """
    Comprehensive status endpoint

    Returns:
    - Health status
    - Performance metrics
    - Active alerts
    - Recent errors
    """
    try:
        health = monitoring_service.get_performance_stats()
        alerts = monitoring_service.get_alert_status()

        return (
            jsonify(
                {
                    "timestamp": health["timestamp"],
                    "status": "healthy" if health["error_rate_percent"] < 5 else "degraded",
                    "performance": {
                        "uptime_hours": health["uptime_hours"],
                        "avg_response_time_ms": health["avg_response_time_ms"],
                        "error_rate_percent": health["error_rate_percent"],
                    },
                    "alerts": {
                        "active_count": alerts["total_active_alerts"],
                        "recent": alerts["active_alerts"][:3],
                    },
                    "capacity": {
                        "active_sessions": health["active_sessions"],
                        "database_connections": health["database_connection_pool"],
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
