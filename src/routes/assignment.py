"""
Lead Assignment Routes

Endpoints for managing lead assignments to sales team.
"""

from flask import Blueprint, jsonify

from src.models.chatbot import Lead
# Lead assignment service (optional - may not exist)
try:
    from src.services.lead_assignment_service import lead_assignment_service
except ImportError:
    lead_assignment_service = None

assignment_bp = Blueprint("assignment", __name__, url_prefix="/api/assignment")


@assignment_bp.route("/assign/<int:lead_id>/<user_id>", methods=["POST"])
def assign_lead(lead_id, user_id):
    """Manually assign lead to specific user"""
    try:
        if lead_assignment_service is None:
            return jsonify({"error": "Assignment service not available"}), 503

        success, message = lead_assignment_service.assign_lead_to_user(lead_id, user_id)

        if success:
            return jsonify({"message": message, "lead_id": lead_id, "user_id": user_id}), 200
        else:
            return jsonify({"error": message}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@assignment_bp.route("/auto-assign/<int:lead_id>", methods=["POST"])
def auto_assign_lead(lead_id):
    """Auto-assign lead to least busy sales user"""
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({"error": "Lead not found"}), 404

        if lead.assigned_to_user_id:
            return (
                jsonify(
                    {
                        "message": "Lead already assigned",
                        "assigned_to": lead.assigned_to_user_id,
                    }
                ),
                200,
            )

        if lead_assignment_service is None:
            return jsonify({"error": "Assignment service not available"}), 503

        success, user_id = lead_assignment_service.auto_assign_lead(lead)

        if success:
            return (
                jsonify(
                    {
                        "message": "Lead auto-assigned successfully",
                        "lead_id": lead_id,
                        "user_id": user_id,
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "Failed to auto-assign lead"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@assignment_bp.route("/users", methods=["GET"])
def get_sales_users():
    """Get list of available sales users"""
    try:
        if lead_assignment_service is None:
            return jsonify({"error": "Assignment service not available"}), 503

        users = lead_assignment_service.get_available_sales_users()
        return jsonify({"users": users}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@assignment_bp.route("/sla-status/<int:lead_id>", methods=["GET"])
def get_sla_status(lead_id):
    """Get SLA status for lead"""
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({"error": "Lead not found"}), 404

        if lead_assignment_service is None:
            return jsonify({"error": "Assignment service not available"}), 503

        status = lead_assignment_service.get_sla_status(lead)
        breached = lead_assignment_service.check_sla_breach(lead)

        return (
            jsonify(
                {
                    "lead_id": lead_id,
                    "assigned_to": lead.assigned_to_user_id,
                    "assigned_at": lead.assigned_at.isoformat() if lead.assigned_at else None,
                    "expected_contact_by": (
                        lead.expected_contact_by.isoformat() if lead.expected_contact_by else None
                    ),
                    "sla_status": status,
                    "sla_breached": breached,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@assignment_bp.route("/breached", methods=["GET"])
def get_breached_slas():
    """Get all leads with breached SLAs"""
    try:
        leads = Lead.query.filter(Lead.assigned_to_user_id.isnot(None)).all()

        if lead_assignment_service is None:
            return jsonify({"error": "Assignment service not available"}), 503

        breached_leads = []
        for lead in leads:
            if lead_assignment_service.check_sla_breach(lead):
                status = lead_assignment_service.get_sla_status(lead)
                breached_leads.append(
                    {
                        "id": lead.id,
                        "name": lead.name,
                        "email": lead.email,
                        "assigned_to": lead.assigned_to_user_id,
                        "breached_by_hours": status.get("breached_by", 0),
                        "expected_contact_by": (
                            lead.expected_contact_by.isoformat()
                            if lead.expected_contact_by
                            else None
                        ),
                    }
                )

        return (
            jsonify(
                {
                    "breached_count": len(breached_leads),
                    "leads": breached_leads,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
