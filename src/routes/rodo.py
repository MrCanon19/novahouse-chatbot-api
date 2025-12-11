"""
RODO/GDPR Routes
Endpoints for data export, deletion, and anonymization.
"""
import logging
from flask import Blueprint, jsonify, request, make_response
from src.services.rodo_service import rodo_service
from src.middleware.security import require_auth

logger = logging.getLogger(__name__)
rodo_bp = Blueprint("rodo", __name__, url_prefix="/api/rodo")


@rodo_bp.route("/inventory", methods=["GET"])
@require_auth
def get_data_inventory():
    """Get data inventory (what data we collect, why, how long)"""
    try:
        inventory = rodo_service.get_data_inventory()
        return jsonify(inventory), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@rodo_bp.route("/export", methods=["POST"])
def export_user_data():
    """
    Export all user data (GDPR right to data portability).
    
    Body: {"email": "user@example.com"}
    """
    try:
        data = request.get_json()
        email = data.get("email")
        
        if not email:
            return jsonify({"error": "email_required", "message": "Email is required"}), 400
        
        export_data = rodo_service.export_user_data(email)  # Supports both email and session_id
        
        if not export_data:
            return jsonify({"error": "not_found", "message": "No data found for this email"}), 404
        
        # Return as JSON
        response = make_response(jsonify(export_data))
        response.headers["Content-Type"] = "application/json"
        response.headers["Content-Disposition"] = f'attachment; filename="rodo_export_{email}_{datetime.now().strftime("%Y%m%d")}.json"'
        return response, 200
        
    except Exception as e:
        logger.error(f"Error exporting user data: {e}")
        return jsonify({"error": str(e)}), 500


@rodo_bp.route("/delete", methods=["POST"])
def delete_user_data():
    """
    Delete all user data (GDPR right to erasure).
    
    Body: {"email": "user@example.com", "confirm": true}
    """
    try:
        data = request.get_json()
        email = data.get("email")
        confirm = data.get("confirm", False)
        
        if not email:
            return jsonify({"error": "email_required", "message": "Email is required"}), 400
        
        if not confirm:
            return jsonify({
                "error": "confirmation_required",
                "message": "Please confirm deletion by setting 'confirm': true"
            }), 400
        
        result = rodo_service.delete_user_data(email)  # Supports both email and session_id
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error deleting user data: {e}")
        return jsonify({"error": str(e)}), 500


@rodo_bp.route("/anonymize-old", methods=["POST"])
@require_auth
def anonymize_old_data():
    """Anonymize old conversations (admin endpoint)"""
    try:
        result = rodo_service.anonymize_old_conversations()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

