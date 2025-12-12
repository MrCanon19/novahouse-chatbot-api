import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from src.integrations.monday_client import MondayClient
from src.models.chatbot import Lead, db
from src.services.email_service import email_service
from src.middleware.security import require_auth

logger = logging.getLogger(__name__)
leads_bp = Blueprint("leads", __name__)

# Admin endpoints require authentication (GET /, export, bulk-update)
# POST / (create_lead) is public - anyone can submit a lead


@leads_bp.route("/", methods=["POST"])
def create_lead():
    """Create a new lead"""
    # Rate limit lead creation per session/IP
    try:
        from src.services.rate_limiter import ensure_rate_limiter

        rate_limiter = ensure_rate_limiter()
        session_id = request.headers.get("X-Session-ID") or request.remote_addr or "default"
        allowed, retry_after = rate_limiter.check_rate_limit(
            session_id, "lead_create", max_requests=5, window_seconds=60
        )
        if not allowed:
            return jsonify({"error": "Rate limit exceeded", "retry_after": retry_after}), 429
    except Exception as e:
        # Fail open if limiter unavailable
        logger.warning(f"Rate limiter check failed, allowing request: {e}")
    # Validate payload using validator
    from src.utils.validators import validate_lead_payload
    from src.exceptions import ValidationError
    
    data = request.get_json()
    if not data:
        raise ValidationError("No data provided")
    
    try:
        validated_data = validate_lead_payload(data)
    except ValidationError as e:
        raise  # Let global error handler catch it
    
    name = validated_data.get("name", "").strip()
    email = validated_data.get("email", "").strip()
    phone = validated_data.get("phone")
    message = validated_data.get("message")

    try:
        lead = Lead(
            name=name.strip(),
            email=email.strip(),
            phone=phone,
            message=message,
            status="new",
            created_at=datetime.now(timezone.utc),
        )

        db.session.add(lead)
        db.session.commit()

        # Sync to Monday.com
        try:
            monday = MondayClient()
            monday_item_id = monday.create_lead_item(
                {
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "message": lead.message,
                }
            )

            if monday_item_id:
                lead.monday_item_id = monday_item_id
                db.session.commit()
                logger.info(f"Lead {lead.id} synced to Monday.com: {monday_item_id}")

        except Exception as e:
            logger.warning(f"Monday.com sync error: {e}", exc_info=True)

        # Send email notifications
        try:
            # Email do admina
            email_service.send_new_lead_notification(
                {
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "message": lead.message,
                    "status": lead.status,
                }
            )

            # Email potwierdzenie do klienta
            email_service.send_lead_confirmation({"name": lead.name, "email": lead.email})
        except Exception as e:
            logger.warning(f"Email notification error: {e}", exc_info=True)

        return (
            jsonify(
                {
                    "id": lead.id,
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "message": lead.message,
                    "status": lead.status,
                    "monday_item_id": lead.monday_item_id,
                    "created_at": lead.created_at.isoformat(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        import logging

        logging.getLogger(__name__).error(f"Lead creation failed: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@leads_bp.route("/", methods=["GET"])
@require_auth
def get_leads():
    """Get all leads (requires authentication)"""
    try:
        leads = Lead.query.order_by(Lead.created_at.desc()).all()

        return (
            jsonify(
                [
                    {
                        "id": lead.id,
                        "name": lead.name,
                        "email": lead.email,
                        "phone": lead.phone,
                        "message": lead.message,
                        "status": lead.status,
                        "monday_item_id": lead.monday_item_id,
                        "created_at": lead.created_at.isoformat(),
                    }
                    for lead in leads
                ]
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@leads_bp.route("/list", methods=["GET"])
@require_auth
def list_leads():
    """Get leads list with stats for dashboard (requires authentication)"""
    try:
        from datetime import datetime, timezone, timedelta
        
        # Get all leads
        all_leads = Lead.query.order_by(Lead.created_at.desc()).all()
        
        # Calculate stats
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today_leads = [l for l in all_leads if l.created_at >= today]
        converted_leads = [l for l in all_leads if l.status == "converted"]
        
        # Format leads for table (limit to 50 most recent)
        leads_data = [
            {
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "message": lead.message,
                "status": lead.status,
                "monday_item_id": lead.monday_item_id,
                "created_at": lead.created_at.isoformat(),
            }
            for lead in all_leads[:50]
        ]
        
        return jsonify({
            "total": len(all_leads),
            "today": len(today_leads),
            "conversions": len(converted_leads),
            "leads": leads_data
        }), 200

    except Exception as e:
        logger.error(f"Error listing leads: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@leads_bp.route("/<int:lead_id>", methods=["GET"])
def get_lead(lead_id):
    """Get a specific lead"""
    try:
        lead = Lead.query.get(lead_id)

        if not lead:
            return jsonify({"error": "Lead not found"}), 404

        return (
            jsonify(
                {
                    "id": lead.id,
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "message": lead.message,
                    "status": lead.status,
                    "monday_item_id": lead.monday_item_id,
                    "created_at": lead.created_at.isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@leads_bp.route("/<int:lead_id>", methods=["PUT"])
def update_lead(lead_id):
    """Update a lead"""
    try:
        lead = Lead.query.get(lead_id)

        if not lead:
            return jsonify({"error": "Lead not found"}), 404

        data = request.get_json()

        if "name" in data:
            lead.name = data["name"]
        if "email" in data:
            lead.email = data["email"]
        if "phone" in data:
            lead.phone = data["phone"]
        if "message" in data:
            lead.message = data["message"]
        if "status" in data:
            lead.status = data["status"]

        db.session.commit()

        return (
            jsonify(
                {
                    "id": lead.id,
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "message": lead.message,
                    "status": lead.status,
                    "monday_item_id": lead.monday_item_id,
                    "created_at": lead.created_at.isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@leads_bp.route("/<int:lead_id>/status", methods=["PATCH"])
def update_lead_status(lead_id):
    """Update lead status and sync with Monday.com"""
    try:
        lead = Lead.query.get(lead_id)

        if not lead:
            return jsonify({"error": "Lead not found"}), 404

        data = request.get_json()
        new_status = data.get("status")

        if not new_status:
            return jsonify({"error": "Status is required"}), 400

        valid_statuses = ["new", "contacted", "qualified", "converted", "lost"]
        if new_status not in valid_statuses:
            return (
                jsonify({"error": f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}),
                400,
            )

        old_status = lead.status
        lead.status = new_status
        db.session.commit()

        # Sync with Monday.com
        if lead.monday_item_id:
            try:
                from src.integrations.monday_client import MondayClient

                monday = MondayClient()
                monday.update_item_status(lead.monday_item_id, new_status)
                print(f"Updated Monday.com item {lead.monday_item_id} status to {new_status}")
            except Exception as e:
                print(f"Monday.com status sync error: {e}")

        return (
            jsonify(
                {
                    "id": lead.id,
                    "old_status": old_status,
                    "new_status": lead.status,
                    "monday_synced": bool(lead.monday_item_id),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@leads_bp.route("/filter", methods=["GET"])
def filter_leads():
    """Filter leads by status, date, package, etc."""
    try:
        query = Lead.query

        # Filter by status
        status = request.args.get("status")
        if status:
            query = query.filter(Lead.status == status)

        # Filter by date range
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if start_date:
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            query = query.filter(Lead.created_at >= start)

        if end_date:
            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            query = query.filter(Lead.created_at <= end)

        # Filter by package (if exists in message/metadata)
        package = request.args.get("package")
        if package:
            query = query.filter(Lead.message.contains(package))

        # Sorting
        sort_by = request.args.get("sort_by", "created_at")
        sort_order = request.args.get("sort_order", "desc")

        if hasattr(Lead, sort_by):
            column = getattr(Lead, sort_by)
            if sort_order == "asc":
                query = query.order_by(column.asc())
            else:
                query = query.order_by(column.desc())

        # Pagination
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 50))

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return (
            jsonify(
                {
                    "leads": [
                        {
                            "id": lead.id,
                            "name": lead.name,
                            "email": lead.email,
                            "phone": lead.phone,
                            "message": lead.message,
                            "status": lead.status,
                            "monday_item_id": lead.monday_item_id,
                            "created_at": lead.created_at.isoformat(),
                        }
                        for lead in paginated.items
                    ],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": paginated.total,
                        "pages": paginated.pages,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@leads_bp.route("/export", methods=["GET"])
@require_auth
def export_leads():
    """Export leads to CSV (requires authentication)"""
    try:
        import csv
        from io import StringIO

        from flask import make_response

        # Get filtered leads (reuse filter logic)
        query = Lead.query

        status = request.args.get("status")
        if status:
            query = query.filter(Lead.status == status)

        start_date = request.args.get("start_date")
        if start_date:
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            query = query.filter(Lead.created_at >= start)

        end_date = request.args.get("end_date")
        if end_date:
            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            query = query.filter(Lead.created_at <= end)

        leads = query.order_by(Lead.created_at.desc()).all()

        # Create CSV
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(
            ["ID", "Data", "Imię", "Email", "Telefon", "Wiadomość", "Status", "Monday.com ID"]
        )

        # Data rows
        for lead in leads:
            writer.writerow(
                [
                    lead.id,
                    lead.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    lead.name,
                    lead.email,
                    lead.phone or "",
                    lead.message or "",
                    lead.status,
                    lead.monday_item_id or "",
                ]
            )

        # Create response
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers["Content-Type"] = "text/csv; charset=utf-8"
        response.headers["Content-Disposition"] = (
            f'attachment; filename=leads_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@leads_bp.route("/bulk-update", methods=["POST"])
@require_auth
def bulk_update_leads():
    """Bulk update lead statuses (requires authentication)"""
    try:
        data = request.get_json()
        lead_ids = data.get("lead_ids", [])
        new_status = data.get("status")

        if not lead_ids or not new_status:
            return jsonify({"error": "lead_ids and status are required"}), 400

        valid_statuses = ["new", "contacted", "qualified", "converted", "lost"]
        if new_status not in valid_statuses:
            return (
                jsonify({"error": f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}),
                400,
            )

        updated_count = 0
        errors = []

        for lead_id in lead_ids:
            try:
                lead = Lead.query.get(lead_id)
                if lead:
                    lead.status = new_status
                    updated_count += 1
                else:
                    errors.append(f"Lead {lead_id} not found")
            except Exception as e:
                errors.append(f"Lead {lead_id}: {str(e)}")

        db.session.commit()

        return (
            jsonify(
                {"success": True, "updated": updated_count, "errors": errors if errors else None}
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
