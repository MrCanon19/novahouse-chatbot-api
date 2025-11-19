from flask import Blueprint, request, jsonify
from src.models.chatbot import db, Lead
from src.integrations.booksy_client import BooksynClient
import os

booking_bp = Blueprint("booking", __name__)


def _check_admin_key():
    """Return None if ok, or (response, status) tuple if unauthorized."""
    admin_key = os.getenv("ADMIN_API_KEY")
    if not admin_key:
        return None
    header = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
    if header == admin_key:
        return None
    return (jsonify({"error": "Unauthorized"}), 401)


@booking_bp.route("/services", methods=["GET"])
def get_services():
    """Get available services from Booksy"""
    try:
        booksy = BooksynClient()

        if not booksy.test_connection():
            return jsonify({"error": "Booksy not configured or unavailable"}), 503

        services = booksy.get_services()

        return jsonify({"services": services, "count": len(services)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/staff", methods=["GET"])
def get_staff():
    """Get available staff from Booksy"""
    try:
        booksy = BooksynClient()

        if not booksy.test_connection():
            return jsonify({"error": "Booksy not configured or unavailable"}), 503

        staff = booksy.get_staff()

        return jsonify({"staff": staff, "count": len(staff)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/available-slots", methods=["GET"])
def get_available_slots():
    """Get available time slots for a service"""
    try:
        service_id = request.args.get("service_id")
        staff_id = request.args.get("staff_id")
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")

        if not service_id:
            return jsonify({"error": "service_id is required"}), 400

        booksy = BooksynClient()

        slots = booksy.get_available_slots(
            service_id=service_id, staff_id=staff_id, date_from=date_from, date_to=date_to
        )

        return jsonify({"service_id": service_id, "slots": slots, "count": len(slots)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/create", methods=["POST"])
def create_booking():
    """Create a new consultation booking"""
    try:
        data = request.get_json()

        required_fields = [
            "client_name",
            "client_email",
            "client_phone",
            "service_id",
            "start_time",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        booksy = BooksynClient()

        booking_id = booksy.create_booking(
            client_name=data["client_name"],
            client_email=data["client_email"],
            client_phone=data["client_phone"],
            service_id=data["service_id"],
            start_time=data["start_time"],
            staff_id=data.get("staff_id"),
            notes=data.get("notes"),
        )

        if not booking_id:
            return jsonify({"error": "Failed to create booking"}), 500

        # Save booking reference to Lead if email provided
        try:
            lead = Lead.query.filter_by(email=data["client_email"]).first()
            if lead:
                # Update lead with booking info
                lead.status = "consultation_booked"
                db.session.commit()
        except Exception as e:
            print(f"Error updating lead: {e}")

        return (
            jsonify(
                {
                    "message": "Booking created successfully",
                    "booking_id": booking_id,
                    "booking_time": data["start_time"],
                    "client_email": data["client_email"],
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/cancel/<booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):
    """Cancel a booking"""
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        booksy = BooksynClient()

        if booksy.cancel_booking(booking_id):
            return (
                jsonify({"message": "Booking cancelled successfully", "booking_id": booking_id}),
                200,
            )
        else:
            return jsonify({"error": "Failed to cancel booking"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/test", methods=["POST"])
def test_booksy():
    """Test Booksy connection"""
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        booksy = BooksynClient()

        if not booksy.test_connection():
            return jsonify({"error": "Failed to connect to Booksy"}), 500

        services = booksy.get_services()
        staff = booksy.get_staff()

        return (
            jsonify(
                {
                    "message": "Booksy connection successful",
                    "api_key_set": bool(booksy.api_key),
                    "business_id_set": bool(booksy.business_id),
                    "services_count": len(services),
                    "staff_count": len(staff),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
