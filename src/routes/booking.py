import os

from flask import Blueprint, jsonify, request
from src.integrations.zencal_client import ZencalClient
from src.models.chatbot import Booking, Lead, db

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


@booking_bp.route("/link", methods=["GET"])
def get_booking_link():
    """
    Pobierz link do rezerwacji Zencal (z pre-filled danymi jeśli dostępne)

    Query params:
        - name: Imię użytkownika (optional)
        - email: Email użytkownika (optional)

    Returns:
        JSON z linkiem do rezerwacji
    """
    try:
        client_name = request.args.get("name")
        client_email = request.args.get("email")

        zencal = ZencalClient()
        booking_link = zencal.get_booking_link(client_name=client_name, client_email=client_email)

        return (
            jsonify(
                {
                    "booking_link": booking_link,
                    "message": "Kliknij w link aby umówić spotkanie z naszym ekspertem",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/available-slots", methods=["GET"])
def get_available_slots():
    """Pobierz dostępne terminy z Zencal"""
    try:
        date = request.args.get("date")  # YYYY-MM-DD

        if not date:
            return jsonify({"error": "date parameter is required (YYYY-MM-DD)"}), 400

        zencal = ZencalClient()
        slots = zencal.get_available_slots(date=date)

        if slots is None:
            return jsonify({"error": "Zencal not configured or unavailable"}), 503

        return jsonify({"date": date, "slots": slots}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/create", methods=["POST"])
def create_booking():
    """Utwórz rezerwację w Zencal"""
    try:
        data = request.get_json()

        required_fields = ["name", "email", "phone", "date", "time"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        zencal = ZencalClient()

        # Utwórz rezerwację w Zencal
        zencal_booking_id = zencal.create_booking(
            {
                "name": data["name"],
                "email": data["email"],
                "phone": data["phone"],
                "date": data["date"],
                "time": data["time"],
                "notes": data.get("notes", ""),
            }
        )

        if not zencal_booking_id:
            return jsonify({"error": "Failed to create booking in Zencal"}), 500

        # Zapisz rezerwację w bazie danych
        booking = Booking(
            client_name=data["name"],
            client_email=data["email"],
            client_phone=data["phone"],
            zencal_booking_id=zencal_booking_id,
            zencal_link=zencal.get_booking_link(data["name"], data["email"]),
            appointment_date=f"{data['date']} {data['time']}",
            status="confirmed",
            notes=data.get("notes"),
        )

        # Połącz z leadem jeśli istnieje
        lead = Lead.query.filter_by(email=data["email"]).first()
        if lead:
            booking.lead_id = lead.id
            lead.status = "consultation_booked"

        db.session.add(booking)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Booking created successfully",
                    "booking_id": booking.id,
                    "zencal_booking_id": zencal_booking_id,
                    "appointment_date": f"{data['date']} {data['time']}",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/cancel/<int:booking_id>", methods=["DELETE"])
def cancel_booking_route(booking_id):
    """Anuluj rezerwację"""
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        zencal = ZencalClient()

        # Anuluj w Zencal jeśli mamy ID
        if booking.zencal_booking_id:
            zencal.cancel_booking(booking.zencal_booking_id)

        # Zmień status w bazie
        booking.status = "cancelled"
        db.session.commit()

        return (
            jsonify({"message": "Booking cancelled successfully", "booking_id": booking_id}),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/test", methods=["POST"])
def test_zencal():
    """Test Zencal connection"""
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        zencal = ZencalClient()

        connection_ok = zencal.test_connection()

        return (
            jsonify(
                {
                    "message": "Zencal connection " + ("successful" if connection_ok else "failed"),
                    "api_key_set": bool(zencal.api_key),
                    "workspace_id_set": bool(zencal.workspace_id),
                    "booking_url": zencal.booking_page_url,
                }
            ),
            200 if connection_ok else 500,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
