"""
Monitoring & Health Routes

Endpoints for application monitoring, alerts, and diagnostics.
Includes extraction quality monitoring and regression detection.
"""

from datetime import datetime

from flask import Blueprint, jsonify

from src.services.extraction_validator import get_safeguard, get_validator
from src.services.monitoring_service import monitoring_service
from src.services.regression_detector import get_detector

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


@monitoring_bp.route("/extraction-quality", methods=["GET"])
def extraction_quality():
    """
    Get extraction quality metrics
    Monitors extract_context() performance and regression detection
    """
    try:
        detector = get_detector()
        trend = detector.get_trend(last_n=50)
        alerts = detector.get_alerts(last_n=20)

        health_status = "healthy"
        if trend.get("avg_success_rate", 100) < 95:
            health_status = "degraded"
        if trend.get("avg_success_rate", 100) < 80:
            health_status = "critical"

        return (
            jsonify(
                {
                    "status": health_status,
                    "timestamp": datetime.now().isoformat(),
                    "metrics": trend,
                    "recent_alerts": alerts,
                    "history_size": len(detector.metrics_history),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@monitoring_bp.route("/regression-history", methods=["GET"])
def regression_history():
    """Get detailed regression history and trend analysis"""
    try:
        detector = get_detector()

        return (
            jsonify(
                {
                    "timestamp": datetime.now().isoformat(),
                    "total_alerts": len(detector.alerts_history),
                    "recent_alerts": detector.get_alerts(last_n=100),
                    "trend_analysis": detector.get_trend(last_n=100),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@monitoring_bp.route("/validation-rules", methods=["GET"])
def validation_rules():
    """Get current validation rules for data extraction"""
    try:
        validator = get_validator()

        return (
            jsonify(
                {
                    "timestamp": datetime.now().isoformat(),
                    "ranges": {
                        "square_meters": validator.VALID_RANGES["square_meters"],
                        "budget": validator.VALID_RANGES["budget"],
                        "lead_score": validator.VALID_RANGES["lead_score"],
                    },
                    "formats": {
                        "email": "valid email address",
                        "phone": "Polish phone number",
                        "name": "Polish name (starts with uppercase)",
                    },
                    "known_cities": list(validator.KNOWN_CITIES),
                    "valid_packages": list(validator.VALID_PACKAGES),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@monitoring_bp.route("/extraction-errors", methods=["GET"])
def extraction_errors():
    """Get summary of extraction errors and safeguard status"""
    try:
        safeguard = get_safeguard()
        detector = get_detector()

        return (
            jsonify(
                {
                    "timestamp": datetime.now().isoformat(),
                    "extraction_safeguard": safeguard.report(),
                    "regression_alerts": {
                        "total": len(detector.alerts_history),
                        "by_type": _group_alerts_by_type(detector.alerts_history),
                        "by_severity": _group_alerts_by_severity(detector.alerts_history),
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _group_alerts_by_type(alerts: list) -> dict:
    """Group alerts by type"""
    grouped = {}
    for alert in alerts:
        alert_type = alert.alert_type if hasattr(alert, "alert_type") else alert.get("alert_type")
        grouped[alert_type] = grouped.get(alert_type, 0) + 1
    return grouped


def _group_alerts_by_severity(alerts: list) -> dict:
    """Group alerts by severity"""
    grouped = {"warning": 0, "critical": 0}
    for alert in alerts:
        severity = alert.severity if hasattr(alert, "severity") else alert.get("severity")
        if severity in grouped:
            grouped[severity] += 1
    return grouped
