"""
Backup & Export API Routes
===========================
RODO-compliant data export and backup management
"""

from flask import Blueprint, jsonify, request, send_file
from src.middleware.security import require_api_key

backup_routes = Blueprint("backup_routes", __name__)


@backup_routes.route("/api/backup/export", methods=["POST"])
@require_api_key
def export_backup():
    """
    Create full database backup

    Body:
        {
            "format": "json" | "csv"
        }

    Returns:
        Download link or file
    """
    try:
        from src.services.backup_service import backup_service

        data = request.get_json() or {}
        format = data.get("format", "json")

        # Create backup
        filepath = backup_service.export_all_data(format=format)

        return jsonify(
            {
                "success": True,
                "message": "Backup created successfully",
                "filepath": filepath,
                "format": format,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@backup_routes.route("/api/backup/list", methods=["GET"])
@require_api_key
def list_backups():
    """
    Get list of available backups

    Returns:
        JSON with backup list
    """
    try:
        from src.services.backup_service import backup_service

        backups = backup_service.get_backup_list()

        return jsonify({"success": True, "data": backups, "count": len(backups)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@backup_routes.route("/api/backup/cleanup", methods=["POST"])
@require_api_key
def cleanup_old_backups():
    """
    Manually trigger cleanup of old backups

    Body:
        {
            "days_to_keep": 30  // Optional, default 30
        }

    Returns:
        JSON with cleanup results
    """
    try:
        from src.services.backup_service import backup_service

        data = request.get_json() or {}
        days_to_keep = data.get("days_to_keep", 30)

        # Clean up old backups
        deleted_count = backup_service.cleanup_old_backups(days_to_keep=days_to_keep)

        return jsonify(
            {
                "success": True,
                "message": "Cleanup completed",
                "deleted_count": deleted_count,
                "days_kept": days_to_keep,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@backup_routes.route("/api/backup/download/<filename>", methods=["GET"])
@require_api_key
def download_backup(filename: str):
    """
    Download specific backup file

    Args:
        filename: Backup filename
    """
    try:
        from src.services.backup_service import backup_service
        import os

        filepath = os.path.join(backup_service.backup_dir, filename)

        if not os.path.exists(filepath):
            return jsonify({"success": False, "error": "Backup not found"}), 404

        return send_file(filepath, as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@backup_routes.route("/api/rodo/export", methods=["POST"])
def rodo_export_user_data():
    """
    RODO Right to Data Portability: Export user data

    Body:
        {
            "user_identifier": "email@example.com" | "phone" | "session_id"
        }

    Returns:
        JSON with all user data
    """
    try:
        from src.services.backup_service import backup_service

        data = request.get_json()
        user_identifier = data.get("user_identifier")

        if not user_identifier:
            return jsonify({"success": False, "error": "user_identifier required"}), 400

        # Export user data
        user_data = backup_service.export_user_data(user_identifier)

        return jsonify({"success": True, "data": user_data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@backup_routes.route("/api/rodo/delete", methods=["POST"])
def rodo_delete_user_data():
    """
    RODO Right to be Forgotten: Delete all user data

    Body:
        {
            "user_identifier": "email@example.com" | "phone" | "session_id",
            "confirm": true
        }

    Returns:
        JSON with deletion summary
    """
    try:
        from src.services.backup_service import backup_service

        data = request.get_json()
        user_identifier = data.get("user_identifier")
        confirm = data.get("confirm", False)

        if not user_identifier:
            return jsonify({"success": False, "error": "user_identifier required"}), 400

        if not confirm:
            return jsonify({"success": False, "error": "Deletion must be confirmed"}), 400

        # Delete user data
        deleted_counts = backup_service.delete_user_data(user_identifier)

        return jsonify(
            {
                "success": True,
                "message": "User data deleted successfully",
                "deleted": deleted_counts,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@backup_routes.route("/api/rodo/consent/check", methods=["POST"])
def check_consent():
    """
    Check if user has active RODO consent

    Body:
        {
            "email": "user@example.com"
        }
    """
    try:
        from src.models.user import RODOConsent

        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"success": False, "error": "email required"}), 400

        # Check consent
        consent = RODOConsent.query.filter_by(email=email).first()

        if not consent:
            return jsonify(
                {"success": True, "has_consent": False, "message": "No consent record found"}
            )

        return jsonify(
            {
                "success": True,
                "has_consent": consent.marketing_consent and consent.data_processing_consent,
                "consent": {
                    "marketing": consent.marketing_consent,
                    "data_processing": consent.data_processing_consent,
                    "created_at": consent.created_at.isoformat() if consent.created_at else None,
                },
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@backup_routes.route("/api/backup/schedule", methods=["POST"])
@require_api_key
def schedule_backup():
    """
    Enable/disable automated backups

    Body:
        {
            "enabled": true
        }
    """
    try:
        from src.services.backup_service import backup_service

        data = request.get_json()
        enabled = data.get("enabled", True)

        if enabled:
            backup_service.schedule_automated_backup()
            message = "Automated backups enabled (daily at 3 AM)"
        else:
            message = "Automated backups disabled"

        return jsonify({"success": True, "message": message, "enabled": enabled})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
