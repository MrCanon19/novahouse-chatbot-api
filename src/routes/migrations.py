"""
HTTP Migration Endpoint - Chat Improvements V2.4
Access via: https://your-app.appspot.com/api/migrations/v24
Requires API_KEY authentication
"""

from flask import Blueprint, jsonify
from src.middleware.security import require_api_key
from src.models.chatbot import db

migration_bp = Blueprint("migrations", __name__)


@migration_bp.route("/v24", methods=["POST"])
@require_api_key
def run_v24_migration():
    """Run Chat Improvements V2.4 database migration"""

    try:
        sqls = [
            "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS conversation_summary TEXT",
            "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS needs_human_review BOOLEAN DEFAULT FALSE",
            "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS followup_count INTEGER DEFAULT 0",
            "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS last_followup_at TIMESTAMP",
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS is_followup BOOLEAN DEFAULT FALSE",
        ]

        results = []
        for sql in sqls:
            try:
                db.session.execute(db.text(sql))
                results.append({"sql": sql[:60] + "...", "status": "success"})
            except Exception as e:
                results.append({"sql": sql[:60] + "...", "status": "error", "error": str(e)})

        db.session.commit()

        return jsonify({"status": "completed", "results": results}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "failed", "error": str(e)}), 500
