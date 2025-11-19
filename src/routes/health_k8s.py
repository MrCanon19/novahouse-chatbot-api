"""
Kubernetes-ready Health Check Endpoints
Implements /health/live, /health/ready, /health/startup for K8s probes
"""

from flask import Blueprint, jsonify
from sqlalchemy import text
import redis
import os
from datetime import datetime

health_bp = Blueprint("health", __name__)

# Track application startup state
_startup_complete = False


def mark_startup_complete():
    """Mark application as fully started"""
    global _startup_complete
    _startup_complete = True


def check_database():
    """Check database connectivity"""
    try:
        from src.database import db

        db.session.execute(text("SELECT 1"))
        return True, "OK"
    except Exception as e:
        return False, str(e)


def check_redis():
    """Check Redis connectivity"""
    try:
        redis_url = os.getenv("REDIS_URL")
        if not redis_url:
            return True, "Not configured (optional)"

        r = redis.from_url(redis_url, socket_connect_timeout=2)
        r.ping()
        return True, "OK"
    except Exception as e:
        return False, str(e)


def check_disk_space():
    """Check available disk space"""
    try:
        import shutil

        total, used, free = shutil.disk_usage("/")
        free_percent = (free / total) * 100

        if free_percent < 10:
            return False, f"Low disk space: {free_percent:.1f}% free"
        return True, f"{free_percent:.1f}% free"
    except Exception as e:
        return False, str(e)


@health_bp.route("/health/live", methods=["GET"])
def liveness():
    """
    Kubernetes liveness probe
    Returns 200 if the application is running

    This should be a lightweight check - if this fails, k8s will restart the pod
    """
    return (
        jsonify(
            {
                "status": "alive",
                "timestamp": datetime.utcnow().isoformat(),
                "service": "novahouse-chatbot-api",
            }
        ),
        200,
    )


@health_bp.route("/health/ready", methods=["GET"])
def readiness():
    """
    Kubernetes readiness probe
    Returns 200 only if the application is ready to serve traffic

    Checks:
    - Database connectivity
    - Redis connectivity (if configured)
    - Disk space

    If this fails, k8s will stop sending traffic to this pod
    """
    checks = {
        "database": check_database(),
        "redis": check_redis(),
        "disk_space": check_disk_space(),
    }

    # Determine overall status
    all_healthy = all(status for status, _ in checks.values())

    response = {
        "status": "ready" if all_healthy else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            name: {"status": "healthy" if status else "unhealthy", "message": message}
            for name, (status, message) in checks.items()
        },
    }

    status_code = 200 if all_healthy else 503
    return jsonify(response), status_code


@health_bp.route("/health/startup", methods=["GET"])
def startup():
    """
    Kubernetes startup probe
    Returns 200 only after the application has completed initialization

    This gives slow-starting applications more time to start before
    liveness checks begin
    """
    if not _startup_complete:
        return (
            jsonify(
                {
                    "status": "starting",
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": "Application is still starting up",
                }
            ),
            503,
        )

    # Once started, verify critical components
    db_ok, db_msg = check_database()

    if not db_ok:
        return (
            jsonify(
                {
                    "status": "starting",
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": f"Database not ready: {db_msg}",
                }
            ),
            503,
        )

    return (
        jsonify(
            {
                "status": "started",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Application has completed startup",
            }
        ),
        200,
    )


@health_bp.route("/health", methods=["GET"])
@health_bp.route("/api/health", methods=["GET"])
def health_check():
    """
    Legacy health check endpoint for backward compatibility
    Returns detailed health information
    """
    checks = {
        "database": check_database(),
        "redis": check_redis(),
        "disk_space": check_disk_space(),
    }

    all_healthy = all(status for status, _ in checks.values())

    response = {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.3.1",
        "environment": os.getenv("FLASK_ENV", "production"),
        "checks": {
            name: {"status": "pass" if status else "fail", "message": message}
            for name, (status, message) in checks.items()
        },
        "uptime": _get_uptime(),
    }

    status_code = 200 if all_healthy else 503
    return jsonify(response), status_code


def _get_uptime():
    """Get application uptime"""
    try:
        from src.main import app_start_time

        uptime_seconds = (datetime.utcnow() - app_start_time).total_seconds()
        return f"{uptime_seconds:.0f}s"
    except Exception:
        return "unknown"
