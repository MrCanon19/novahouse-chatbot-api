from flask import Blueprint, jsonify
from src.models.chatbot import db, Intent, Entity

health_bp = Blueprint("health", __name__)


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


@health_bp.route("/init-db", methods=["POST"])
def init_database():
    try:
        db.create_all()
        return {"success": True, "message": "Database initialized"}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500
