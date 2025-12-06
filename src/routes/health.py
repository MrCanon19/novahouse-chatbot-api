import os
from datetime import datetime, timezone

from flask import Blueprint, jsonify

from src.models.chatbot import Entity, Intent, db

health_bp = Blueprint("health", __name__)
APP_START_TIME = datetime.now(timezone.utc)

VERSION_ENV_ORDER = [
    "RELEASE_REVISION",
    "COMMIT_SHA",
    "K_REVISION",
    "GAE_VERSION",
    "GAE_SERVICE",
]
ENVIRONMENT_ENV_ORDER = ["FLASK_ENV", "APP_ENV", "ENVIRONMENT", "ENV"]


def _get_uptime_seconds() -> int:
    return int((datetime.now(timezone.utc) - APP_START_TIME).total_seconds())


def _get_service_version() -> str:
    for env_name in VERSION_ENV_ORDER:
        value = os.getenv(env_name)
        if value and value.strip():
            return value.strip()

    return "dev"


def _get_environment_name() -> str:
    for env_name in ENVIRONMENT_ENV_ORDER:
        value = os.getenv(env_name)
        if value and value.strip():
            return value.strip()

    return "development"


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint dla Google Cloud Platform"""
    try:
        # Sprawdzenie połączenia z bazą danych
        intent_count = Intent.query.count()
        entity_count = Entity.query.count()

        return (
            jsonify(
                {
                    "status": "healthy",
                    "database": "connected",
                    "intents_loaded": intent_count,
                    "entities_loaded": entity_count,
                    "service": "novahouse-chatbot",
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "unhealthy", "error": str(e), "service": "novahouse-chatbot"}),
            500,
        )


@health_bp.route("/_ah/health", methods=["GET"])
def app_engine_health():
    """Health check endpoint specjalnie dla App Engine"""
    return health_check()


@health_bp.route("/ready", methods=["GET"])
def readiness_check():
    """Readiness check endpoint"""
    try:
        # Sprawdzenie czy aplikacja jest gotowa do obsługi ruchu
        intent_count = Intent.query.count()

        if intent_count > 0:
            return jsonify({"status": "ready", "intents_loaded": intent_count}), 200
        else:
            return jsonify({"status": "not_ready", "reason": "No intents loaded"}), 503

    except Exception as e:
        return jsonify({"status": "not_ready", "error": str(e)}), 503


@health_bp.route("/status", methods=["GET"])
def detailed_status():
    """Return a richer status payload for runtime diagnostics."""

    try:
        intent_count = Intent.query.count()
        entity_count = Entity.query.count()

        return (
            jsonify(
                {
                    "status": "healthy",
                    "service": "novahouse-chatbot",
                    "uptime_seconds": _get_uptime_seconds(),
                    "environment": _get_environment_name(),
                    "version": _get_service_version(),
                    "database": {
                        "status": "connected",
                        "intents_loaded": intent_count,
                        "entities_loaded": entity_count,
                    },
                }
            ),
            200,
        )

    except Exception as exc:  # pragma: no cover - defensive path
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "service": "novahouse-chatbot",
                    "error": str(exc),
                    "uptime_seconds": _get_uptime_seconds(),
                }
            ),
            500,
        )


@health_bp.route("/init-db", methods=["POST"])
def init_database():
    try:
        db.create_all()
        return {"success": True, "message": "Database initialized"}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500
