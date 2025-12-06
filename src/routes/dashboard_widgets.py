"""
Dashboard Widgets API
=====================
Real-time metrics and custom widgets
"""

from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy import desc, func
from src.middleware.security import require_api_key

dashboard_widgets = Blueprint("dashboard_widgets", __name__)


@dashboard_widgets.route("/api/widgets/metrics/summary", methods=["GET"])
@require_api_key
def get_metrics_summary():
    """
    Get summary metrics for dashboard

    Returns:
        JSON with key metrics (conversations, leads, bookings, conversions)
    """
    try:
        from src.database import db
        from src.models.analytics import Booking, Lead
        from src.models.chatbot import ChatSession, Message

        # Time range (default: last 30 days)
        days = int(request.args.get("days", 30))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Total conversations
        total_conversations = (
            db.session.query(ChatSession).filter(ChatSession.created_at >= start_date).count()
        )

        # Total messages
        total_messages = db.session.query(Message).filter(Message.created_at >= start_date).count()

        # Total leads
        total_leads = db.session.query(Lead).filter(Lead.created_at >= start_date).count()

        # Total bookings
        total_bookings = db.session.query(Booking).filter(Booking.created_at >= start_date).count()

        # Conversion rate
        conversion_rate = (
            (total_bookings / total_conversations * 100) if total_conversations > 0 else 0
        )

        return jsonify(
            {
                "success": True,
                "data": {
                    "conversations": total_conversations,
                    "messages": total_messages,
                    "leads": total_leads,
                    "bookings": total_bookings,
                    "conversion_rate": round(conversion_rate, 2),
                    "period_days": days,
                },
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_widgets.route("/api/widgets/metrics/timeline", methods=["GET"])
@require_api_key
def get_metrics_timeline():
    """
    Get timeline data for charts (daily/weekly/monthly)

    Returns:
        JSON with time-series data
    """
    try:
        from src.database import db
        from src.models.analytics import Booking, Lead
        from src.models.chatbot import ChatSession

        # Time range
        days = int(request.args.get("days", 30))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Group by day
        conversations_by_day = (
            db.session.query(
                func.date(ChatSession.created_at).label("date"),
                func.count(ChatSession.id).label("count"),
            )
            .filter(ChatSession.created_at >= start_date)
            .group_by(func.date(ChatSession.created_at))
            .order_by("date")
            .all()
        )

        leads_by_day = (
            db.session.query(
                func.date(Lead.created_at).label("date"), func.count(Lead.id).label("count")
            )
            .filter(Lead.created_at >= start_date)
            .group_by(func.date(Lead.created_at))
            .order_by("date")
            .all()
        )

        bookings_by_day = (
            db.session.query(
                func.date(Booking.created_at).label("date"), func.count(Booking.id).label("count")
            )
            .filter(Booking.created_at >= start_date)
            .group_by(func.date(Booking.created_at))
            .order_by("date")
            .all()
        )

        return jsonify(
            {
                "success": True,
                "data": {
                    "conversations": [
                        {"date": str(row.date), "count": row.count} for row in conversations_by_day
                    ],
                    "leads": [{"date": str(row.date), "count": row.count} for row in leads_by_day],
                    "bookings": [
                        {"date": str(row.date), "count": row.count} for row in bookings_by_day
                    ],
                },
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_widgets.route("/api/widgets/top/intents", methods=["GET"])
@require_api_key
def get_top_intents():
    """
    Get top detected intents

    Returns:
        JSON with intent distribution
    """
    try:
        from src.database import db
        from src.models.chatbot import Message

        # Time range
        days = int(request.args.get("days", 30))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Group by intent
        top_intents = (
            db.session.query(Message.intent, func.count(Message.id).label("count"))
            .filter(Message.created_at >= start_date, Message.intent.isnot(None))
            .group_by(Message.intent)
            .order_by(desc("count"))
            .limit(10)
            .all()
        )

        return jsonify(
            {
                "success": True,
                "data": [{"intent": row.intent, "count": row.count} for row in top_intents],
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_widgets.route("/api/widgets/top/packages", methods=["GET"])
@require_api_key
def get_top_packages():
    """
    Get most popular design packages

    Returns:
        JSON with package distribution
    """
    try:
        from src.database import db
        from src.models.analytics import Lead

        # Time range
        days = int(request.args.get("days", 30))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Group by package
        top_packages = (
            db.session.query(Lead.interested_package, func.count(Lead.id).label("count"))
            .filter(Lead.created_at >= start_date, Lead.interested_package.isnot(None))
            .group_by(Lead.interested_package)
            .order_by(desc("count"))
            .all()
        )

        return jsonify(
            {
                "success": True,
                "data": [
                    {"package": row.interested_package, "count": row.count} for row in top_packages
                ],
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_widgets.route("/api/widgets/active/sessions", methods=["GET"])
@require_api_key
def get_active_sessions():
    """
    Get active chat sessions (last 5 minutes)

    Returns:
        JSON with active session count
    """
    try:
        from src.database import db
        from src.models.chatbot import ChatSession

        # Last 5 minutes
        threshold = datetime.now(timezone.utc) - timedelta(minutes=5)

        active_count = (
            db.session.query(ChatSession).filter(ChatSession.last_activity >= threshold).count()
        )

        # Also get from WebSocket connections
        try:
            from src.services.websocket_service import get_active_connections_count

            ws_count = get_active_connections_count()
        except Exception:
            ws_count = 0

        return jsonify(
            {
                "success": True,
                "data": {
                    "active_sessions": active_count,
                    "websocket_connections": ws_count,
                    "total": max(active_count, ws_count),
                },
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_widgets.route("/api/widgets/response/times", methods=["GET"])
@require_api_key
def get_response_times():
    """
    Get average response times

    Returns:
        JSON with response time metrics
    """
    try:
        from src.database import db
        from src.models.chatbot import Message

        # Time range
        days = int(request.args.get("days", 7))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Calculate average response time (mock - would need message timestamps)
        bot_messages = (
            db.session.query(Message)
            .filter(Message.created_at >= start_date, Message.sender == "bot")
            .count()
        )

        # Mock calculation (replace with actual timing logic)
        avg_response_time = 1.2  # seconds

        return jsonify(
            {
                "success": True,
                "data": {
                    "average_response_time": avg_response_time,
                    "total_bot_messages": bot_messages,
                    "period_days": days,
                },
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_widgets.route("/api/widgets/satisfaction/scores", methods=["GET"])
@require_api_key
def get_satisfaction_scores():
    """
    Get satisfaction ratings distribution

    Returns:
        JSON with rating counts
    """
    try:
        from src.database import db
        from src.models.chatbot import ChatSession

        # Time range
        days = int(request.args.get("days", 30))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Group by rating
        ratings = (
            db.session.query(ChatSession.rating, func.count(ChatSession.id).label("count"))
            .filter(ChatSession.created_at >= start_date, ChatSession.rating.isnot(None))
            .group_by(ChatSession.rating)
            .order_by(ChatSession.rating)
            .all()
        )

        # Calculate average
        total_ratings = sum(row.count for row in ratings)
        weighted_sum = sum(row.rating * row.count for row in ratings)
        avg_rating = (weighted_sum / total_ratings) if total_ratings > 0 else 0

        return jsonify(
            {
                "success": True,
                "data": {
                    "distribution": [{"rating": row.rating, "count": row.count} for row in ratings],
                    "average": round(avg_rating, 2),
                    "total": total_ratings,
                },
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@dashboard_widgets.route("/api/widgets/custom", methods=["POST"])
@require_api_key
def save_custom_widget():
    """
    Save custom widget configuration

    Body:
        {
            "widget_id": "custom_1",
            "type": "chart",
            "config": {...}
        }
    """
    try:
        data = request.get_json()

        # In production, save to database
        # For now, return success

        return jsonify(
            {"success": True, "message": "Custom widget saved", "widget_id": data.get("widget_id")}
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
