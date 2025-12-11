"""
Lead Verification Routes

Endpoints for email and phone verification.
"""

from flask import Blueprint, jsonify, request

from src.models.chatbot import Lead
# Lead verification service (optional - may not exist)
try:
    from src.services.lead_verification_service import lead_verification_service
except ImportError:
    lead_verification_service = None

verification_bp = Blueprint("verification", __name__, url_prefix="/api/verification")


@verification_bp.route("/send-email/<int:lead_id>", methods=["POST"])
def send_email_verification(lead_id):
    """Send email verification to lead"""
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({"error": "Lead not found"}), 404

        if lead.email_verified:
            return jsonify({"message": "Email already verified"}), 200

        if lead_verification_service is None:
            return jsonify({"error": "Verification service not available"}), 503

        success, message = lead_verification_service.send_email_verification(lead)

        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": message}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@verification_bp.route("/verify-email", methods=["GET"])
def verify_email():
    """Verify email token (from link click)"""
    try:
        lead_id = request.args.get("lead_id", type=int)
        token = request.args.get("token", type=str)

        if not lead_id or not token:
            return jsonify({"error": "Missing lead_id or token"}), 400

        if lead_verification_service is None:
            return jsonify({"error": "Verification service not available"}), 503

        success, message = lead_verification_service.verify_email_token(lead_id, token)

        if success:
            return (
                jsonify(
                    {
                        "message": message,
                        "status": "verified",
                        "lead_id": lead_id,
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": message}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@verification_bp.route("/send-sms/<int:lead_id>", methods=["POST"])
def send_sms_verification(lead_id):
    """Send SMS verification code to lead"""
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({"error": "Lead not found"}), 404

        if lead.phone_verified:
            return jsonify({"message": "Phone already verified"}), 200

        if lead_verification_service is None:
            return jsonify({"error": "Verification service not available"}), 503

        success, message = lead_verification_service.send_phone_verification(lead)

        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": message}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@verification_bp.route("/verify-sms", methods=["POST"])
def verify_sms():
    """Verify SMS code"""
    try:
        data = request.get_json()
        lead_id = data.get("lead_id")
        code = data.get("code")

        if not lead_id or not code:
            return jsonify({"error": "Missing lead_id or code"}), 400

        if lead_verification_service is None:
            return jsonify({"error": "Verification service not available"}), 503

        success, message = lead_verification_service.verify_phone_code(lead_id, code)

        if success:
            return (
                jsonify(
                    {
                        "message": message,
                        "status": "verified",
                        "lead_id": lead_id,
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": message}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@verification_bp.route("/status/<int:lead_id>", methods=["GET"])
def verification_status(lead_id):
    """Get verification status for lead"""
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({"error": "Lead not found"}), 404

        return (
            jsonify(
                {
                    "lead_id": lead_id,
                    "email": lead.email,
                    "email_verified": lead.email_verified,
                    "email_verified_at": (
                        lead.email_verified_at.isoformat() if lead.email_verified_at else None
                    ),
                    "phone": lead.phone,
                    "phone_verified": lead.phone_verified,
                    "phone_verified_at": (
                        lead.phone_verified_at.isoformat() if lead.phone_verified_at else None
                    ),
                    "fully_verified": (lead.email_verified or lead.phone_verified),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
