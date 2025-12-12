import os

from flask import Blueprint, jsonify, request

# Zencal integration (optional)
try:
    from src.integrations.zencal_client import ZencalClient
except ImportError:
    ZencalClient = None
from src.models.chatbot import Booking, Lead, TeamMember, db

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
        - consultant_id: ID konsultanta (optional) - jeśli chcemy przypisać do konkretnego konsultanta

    Returns:
        JSON z linkiem do rezerwacji
    """
    try:
        client_name = request.args.get("name")
        client_email = request.args.get("email")
        consultant_id = request.args.get("consultant_id", type=int)

        consultant_booking_url = None
        if consultant_id:
            consultant = TeamMember.query.get(consultant_id)
            if consultant and consultant.is_active:
                consultant_booking_url = consultant.zencal_booking_url

        zencal = ZencalClient()
        booking_link = zencal.get_booking_link(
            client_name=client_name,
            client_email=client_email,
            consultant_booking_url=consultant_booking_url,
        )

        return (
            jsonify(
                {
                    "booking_link": booking_link,
                    "message": "Kliknij w link aby umówić spotkanie z naszym ekspertem",
                    "consultant_id": consultant_id,
                }
            ),
            200,
        )

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting booking link: {e}", exc_info=True)
        return jsonify({"error": "internal_error", "message": "Failed to get booking link"}), 500


@booking_bp.route("/available-slots", methods=["GET"])
def get_available_slots():
    """Pobierz dostępne terminy z Zencal"""
    try:
        date = request.args.get("date")  # YYYY-MM-DD

        if not date:
            return jsonify({"error": "date parameter is required (YYYY-MM-DD)"}), 400

        if ZencalClient is None:
            return jsonify({"error": "Zencal integration not available"}), 503

        zencal = ZencalClient()
        slots = zencal.get_available_slots(date=date)

        if slots is None:
            return jsonify({"error": "Zencal not configured or unavailable"}), 503

        return jsonify({"date": date, "slots": slots}), 200

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting booking link: {e}", exc_info=True)
        return jsonify({"error": "internal_error", "message": "Failed to get booking link"}), 500


@booking_bp.route("/create", methods=["POST"])
def create_booking():
    """Utwórz rezerwację w Zencal"""
    try:
        data = request.get_json()

        required_fields = ["name", "email", "phone", "date", "time"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        if ZencalClient is None:
            return jsonify({"error": "Zencal integration not available"}), 503

        zencal = ZencalClient()

        # Sprawdź czy przypisano konsultanta
        consultant_id = data.get("consultant_id")
        consultant = None
        consultant_booking_url = None
        zencal_user_id = None

        if consultant_id:
            consultant = TeamMember.query.get(consultant_id)
            if consultant and consultant.is_active:
                consultant_booking_url = consultant.zencal_booking_url
                zencal_user_id = consultant.zencal_user_id

        # Utwórz rezerwację w Zencal
        zencal_booking_id = zencal.create_booking(
            {
                "name": data["name"],
                "email": data["email"],
                "phone": data["phone"],
                "date": data["date"],
                "time": data["time"],
                "notes": data.get("notes", ""),
                "zencal_user_id": zencal_user_id,
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
            zencal_link=zencal.get_booking_link(
                data["name"], data["email"], consultant_booking_url
            ),
            appointment_date=f"{data['date']} {data['time']}",
            status="confirmed",
            notes=data.get("notes"),
            assigned_to_consultant_id=consultant_id if consultant else None,
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

        if ZencalClient is None:
            return jsonify({"error": "Zencal integration not available"}), 503

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

        if ZencalClient is None:
            return jsonify({"error": "Zencal integration not available", "available": False}), 503

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
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting booking link: {e}", exc_info=True)
        return jsonify({"error": "internal_error", "message": "Failed to get booking link"}), 500


@booking_bp.route("/list", methods=["GET"])
def list_bookings():
    """
    Lista rezerwacji z możliwością filtrowania po konsultancie

    Query params:
        - consultant_id: ID konsultanta (optional) - filtruj po konsultancie
        - status: Status rezerwacji (optional) - pending, confirmed, completed, cancelled
        - limit: Limit wyników (optional, default: 50)
        - offset: Offset wyników (optional, default: 0)

    Returns:
        JSON z listą rezerwacji
    """
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        consultant_id = request.args.get("consultant_id", type=int)
        status = request.args.get("status")
        limit = request.args.get("limit", type=int, default=50)
        offset = request.args.get("offset", type=int, default=0)

        # Query z filtrowaniem
        query = Booking.query

        if consultant_id:
            query = query.filter_by(assigned_to_consultant_id=consultant_id)

        if status:
            query = query.filter_by(status=status)

        # Sortuj po dacie spotkania (najnowsze pierwsze)
        query = query.order_by(Booking.appointment_date.desc())

        # Paginacja
        total = query.count()
        bookings = query.limit(limit).offset(offset).all()

        return (
            jsonify(
                {
                    "bookings": [booking.to_dict() for booking in bookings],
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                }
            ),
            200,
        )

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting booking link: {e}", exc_info=True)
        return jsonify({"error": "internal_error", "message": "Failed to get booking link"}), 500


# ==================== TEAM MEMBERS (KONSULTANCI) ====================


@booking_bp.route("/team-members", methods=["GET"])
def list_team_members():
    """
    Lista wszystkich aktywnych konsultantów

    Returns:
        JSON z listą konsultantów
    """
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        active_only = request.args.get("active_only", "true").lower() == "true"

        query = TeamMember.query
        if active_only:
            query = query.filter_by(is_active=True)

        members = query.order_by(TeamMember.name).all()

        return jsonify({"team_members": [member.to_dict() for member in members]}), 200

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting booking link: {e}", exc_info=True)
        return jsonify({"error": "internal_error", "message": "Failed to get booking link"}), 500


@booking_bp.route("/team-members", methods=["POST"])
def create_team_member():
    """
    Utwórz nowego konsultanta

    Body:
        - name: Imię i nazwisko (required)
        - email: Email (required, unique)
        - phone: Telefon (optional)
        - zencal_user_id: ID użytkownika w Zencal (optional)
        - zencal_booking_url: Unikalny URL do rezerwacji (optional)

    Returns:
        JSON z utworzonym konsultantem
    """
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        data = request.get_json()

        required_fields = ["name", "email"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        # Sprawdź czy email już istnieje
        existing = TeamMember.query.filter_by(email=data["email"]).first()
        if existing:
            return jsonify({"error": "Email already exists"}), 400

        member = TeamMember(
            name=data["name"],
            email=data["email"],
            phone=data.get("phone"),
            zencal_user_id=data.get("zencal_user_id"),
            zencal_booking_url=data.get("zencal_booking_url"),
            is_active=data.get("is_active", True),
        )

        db.session.add(member)
        db.session.commit()

        return jsonify({"team_member": member.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/team-members/<int:member_id>", methods=["GET"])
def get_team_member(member_id):
    """
    Pobierz szczegóły konsultanta

    Returns:
        JSON z konsultantem
    """
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        member = TeamMember.query.get(member_id)
        if not member:
            return jsonify({"error": "Team member not found"}), 404

        return jsonify({"team_member": member.to_dict()}), 200

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting booking link: {e}", exc_info=True)
        return jsonify({"error": "internal_error", "message": "Failed to get booking link"}), 500


@booking_bp.route("/team-members/<int:member_id>", methods=["PUT"])
def update_team_member(member_id):
    """
    Zaktualizuj konsultanta

    Body:
        - name: Imię i nazwisko (optional)
        - email: Email (optional)
        - phone: Telefon (optional)
        - zencal_user_id: ID użytkownika w Zencal (optional)
        - zencal_booking_url: Unikalny URL do rezerwacji (optional)
        - is_active: Czy aktywny (optional)

    Returns:
        JSON z zaktualizowanym konsultantem
    """
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        member = TeamMember.query.get(member_id)
        if not member:
            return jsonify({"error": "Team member not found"}), 404

        data = request.get_json()

        if "name" in data:
            member.name = data["name"]
        if "email" in data:
            # Sprawdź czy email nie jest już używany przez innego konsultanta
            existing = TeamMember.query.filter_by(email=data["email"]).first()
            if existing and existing.id != member_id:
                return jsonify({"error": "Email already exists"}), 400
            member.email = data["email"]
        if "phone" in data:
            member.phone = data["phone"]
        if "zencal_user_id" in data:
            member.zencal_user_id = data["zencal_user_id"]
        if "zencal_booking_url" in data:
            member.zencal_booking_url = data["zencal_booking_url"]
        if "is_active" in data:
            member.is_active = data["is_active"]

        db.session.commit()

        return jsonify({"team_member": member.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/team-members/<int:member_id>", methods=["DELETE"])
def delete_team_member(member_id):
    """
    Usuń konsultanta (soft delete - ustawia is_active=False)

    Returns:
        JSON z potwierdzeniem
    """
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        member = TeamMember.query.get(member_id)
        if not member:
            return jsonify({"error": "Team member not found"}), 404

        # Sprawdź czy ma przypisane rezerwacje
        active_bookings = Booking.query.filter_by(
            assigned_to_consultant_id=member_id, status="confirmed"
        ).count()

        if active_bookings > 0:
            # Soft delete - tylko deaktywuj
            member.is_active = False
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": "Team member deactivated (has active bookings)",
                        "team_member": member.to_dict(),
                    }
                ),
                200,
            )

        # Hard delete jeśli nie ma rezerwacji
        db.session.delete(member)
        db.session.commit()

        return jsonify({"message": "Team member deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@booking_bp.route("/team-members/<int:member_id>/bookings", methods=["GET"])
def get_consultant_bookings(member_id):
    """
    Pobierz wszystkie rezerwacje przypisane do konkretnego konsultanta

    Query params:
        - status: Status rezerwacji (optional)
        - limit: Limit wyników (optional, default: 50)
        - offset: Offset wyników (optional, default: 0)

    Returns:
        JSON z listą rezerwacji konsultanta
    """
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        member = TeamMember.query.get(member_id)
        if not member:
            return jsonify({"error": "Team member not found"}), 404

        status = request.args.get("status")
        limit = request.args.get("limit", type=int, default=50)
        offset = request.args.get("offset", type=int, default=0)

        query = Booking.query.filter_by(assigned_to_consultant_id=member_id)

        if status:
            query = query.filter_by(status=status)

        query = query.order_by(Booking.appointment_date.desc())

        total = query.count()
        bookings = query.limit(limit).offset(offset).all()

        return (
            jsonify(
                {
                    "consultant": member.to_dict(),
                    "bookings": [booking.to_dict() for booking in bookings],
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                }
            ),
            200,
        )

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting booking link: {e}", exc_info=True)
        return jsonify({"error": "internal_error", "message": "Failed to get booking link"}), 500


@booking_bp.route("/sync-zencal-team", methods=["POST"])
def sync_zencal_team():
    """
    Synchronizuj członków zespołu z Zencal API

    Returns:
        JSON z wynikiem synchronizacji
    """
    try:
        # Admin key check
        auth_error = _check_admin_key()
        if auth_error:
            return auth_error

        if ZencalClient is None:
            return jsonify({"error": "Zencal integration not available"}), 503

        zencal = ZencalClient()
        zencal_members = zencal.get_team_members()

        if not zencal_members:
            return jsonify({"error": "Failed to fetch team members from Zencal"}), 500

        synced_count = 0
        created_count = 0
        updated_count = 0

        for zencal_member in zencal_members:
            # Szukaj po email lub zencal_user_id
            member = TeamMember.query.filter_by(
                zencal_user_id=zencal_member.get("id")
            ).first()

            if not member:
                # Sprawdź po email
                member = TeamMember.query.filter_by(
                    email=zencal_member.get("email")
                ).first()

            if member:
                # Aktualizuj istniejącego
                member.zencal_user_id = zencal_member.get("id")
                member.zencal_booking_url = zencal_member.get("booking_url")
                if not member.name:
                    member.name = zencal_member.get("name", "")
                updated_count += 1
            else:
                # Utwórz nowego
                member = TeamMember(
                    name=zencal_member.get("name", ""),
                    email=zencal_member.get("email", ""),
                    zencal_user_id=zencal_member.get("id"),
                    zencal_booking_url=zencal_member.get("booking_url"),
                    is_active=True,
                )
                db.session.add(member)
                created_count += 1

            synced_count += 1

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Team members synced successfully",
                    "synced": synced_count,
                    "created": created_count,
                    "updated": updated_count,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
