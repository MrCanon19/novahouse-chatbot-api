from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import func

from src.models.analytics import ChatAnalytics, IntentAnalytics, PerformanceMetrics, UserEngagement
from src.models.chatbot import Conversation, Lead, db

analytics_bp = Blueprint("analytics", __name__)


def _clamp_days(raw_days: int, default: int = 7, max_days: int = 31) -> int:
    """Sanitize days parameter to prevent heavy full-table scans."""
    if raw_days is None:
        return default
    return max(1, min(raw_days, max_days))


@analytics_bp.route("/overview", methods=["GET"])
def get_overview():
    """Pobierz ogólny przegląd analityki"""
    # Parametry zapytania
    days = _clamp_days(request.args.get("days", 7, type=int))
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    def _safe_scalar(query_fn, fallback=0):
        """Execute a query and log errors instead of bubbling 500."""
        try:
            return query_fn() or fallback
        except Exception as exc:  # pragma: no cover - defensive logging path
            current_app.logger.exception("analytics_overview_scalar_failed", extra={"days": days})
            return fallback

    # Statystyki konwersacji
    total_conversations = _safe_scalar(
        lambda: Conversation.query.filter(Conversation.timestamp >= start_date).count(), fallback=0
    )

    # Statystyki leadów
    total_leads = _safe_scalar(
        lambda: Lead.query.filter(Lead.created_at >= start_date).count(), fallback=0
    )

    # Unikalne sesje - dla małych zakresów (<= 3 dni) użyj prostego count distinct
    # dla większych zwróć approximate estimate żeby uniknąć timeoutu
    if days <= 3:
        unique_sessions = _safe_scalar(
            lambda: int(
                db.session.query(func.count(func.distinct(Conversation.session_id)))
                .filter(Conversation.timestamp >= start_date)
                .scalar()
                or 0
            ),
            fallback=0,
        )
    else:
        # Dla większych zakresów: użyj szybkiego przybliżenia (count / avg msg per session ~5)
        total_conv = _safe_scalar(
            lambda: db.session.query(func.count(Conversation.id))
            .filter(Conversation.timestamp >= start_date)
            .scalar(),
            fallback=0,
        )
        # jeśli nie mamy danych, uniknij dzielenia przez zero – zwróć 0 sesji
        unique_sessions = max(0, int((total_conv or 0) / 5))

    # Średni czas trwania sesji
    avg_session_duration = _safe_scalar(
        lambda: db.session.query(func.avg(UserEngagement.session_duration_seconds))
        .filter(UserEngagement.first_interaction >= start_date)
        .scalar(),
        fallback=0.0,
    )
    avg_session_duration = float(avg_session_duration)

    # Współczynnik konwersji
    conversion_rate = (total_leads / unique_sessions * 100) if unique_sessions > 0 else 0

    # Top intencje
    def _top_intents_query():
        return (
            db.session.query(
                IntentAnalytics.intent_name,
                func.sum(IntentAnalytics.trigger_count).label("total_triggers"),
            )
            .filter(IntentAnalytics.date >= start_date.date())
            .group_by(IntentAnalytics.intent_name)
            .order_by(func.sum(IntentAnalytics.trigger_count).desc())
            .limit(5)
            .all()
        )

    top_intents = _safe_scalar(_top_intents_query, fallback=[])

    return jsonify(
        {
            "status": "success",
            "period_days": days,
            "overview": {
                "total_conversations": total_conversations,
                "total_leads": total_leads,
                "unique_sessions": unique_sessions,
                "avg_session_duration_seconds": (
                    round(avg_session_duration, 2) if avg_session_duration else 0
                ),
                "conversion_rate_percent": round(conversion_rate, 2),
                "top_intents": [
                    {"intent": intent, "count": count} for intent, count in top_intents
                ],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


@analytics_bp.route("/conversations", methods=["GET"])
def get_conversation_analytics():
    """Pobierz analitykę konwersacji"""
    try:
        days = _clamp_days(request.args.get("days", 7, type=int))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Konwersacje według dnia
        conversations_by_day = (
            db.session.query(
                func.date(Conversation.timestamp).label("date"),
                func.count(Conversation.id).label("count"),
            )
            .filter(Conversation.timestamp >= start_date)
            .group_by(func.date(Conversation.timestamp))
            .order_by(func.date(Conversation.timestamp))
            .all()
        )

        # Analityka czatu
        chat_analytics = ChatAnalytics.query.filter(ChatAnalytics.timestamp >= start_date).all()

        # Statystyki sentymentu
        sentiment_stats = (
            db.session.query(ChatAnalytics.sentiment, func.count(ChatAnalytics.id).label("count"))
            .filter(ChatAnalytics.timestamp >= start_date, ChatAnalytics.sentiment.isnot(None))
            .group_by(ChatAnalytics.sentiment)
            .all()
        )

        return jsonify(
            {
                "status": "success",
                "conversations_by_day": [
                    {"date": str(date), "count": count} for date, count in conversations_by_day
                ],
                "sentiment_distribution": [
                    {"sentiment": sentiment, "count": count} for sentiment, count in sentiment_stats
                ],
                "total_analyzed": len(chat_analytics),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/engagement", methods=["GET"])
def get_engagement_analytics():
    """Pobierz analitykę zaangażowania użytkowników"""
    try:
        days = _clamp_days(request.args.get("days", 7, type=int))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Zaangażowanie użytkowników
        engagements = UserEngagement.query.filter(
            UserEngagement.first_interaction >= start_date
        ).all()

        # Statystyki urządzeń
        device_stats = (
            db.session.query(
                UserEngagement.device_type, func.count(UserEngagement.id).label("count")
            )
            .filter(
                UserEngagement.first_interaction >= start_date,
                UserEngagement.device_type.isnot(None),
            )
            .group_by(UserEngagement.device_type)
            .all()
        )

        # Statystyki konwersji
        conversion_stats = (
            db.session.query(
                UserEngagement.conversion_event, func.count(UserEngagement.id).label("count")
            )
            .filter(
                UserEngagement.first_interaction >= start_date,
                UserEngagement.conversion_event.isnot(None),
            )
            .group_by(UserEngagement.conversion_event)
            .all()
        )

        # Średnie metryki
        avg_messages = (
            db.session.query(func.avg(UserEngagement.total_messages))
            .filter(UserEngagement.first_interaction >= start_date)
            .scalar()
        )

        avg_duration = (
            db.session.query(func.avg(UserEngagement.session_duration_seconds))
            .filter(UserEngagement.first_interaction >= start_date)
            .scalar()
        )

        return jsonify(
            {
                "status": "success",
                "total_sessions": len(engagements),
                "device_distribution": [
                    {"device": device, "count": count} for device, count in device_stats
                ],
                "conversion_events": [
                    {"event": event, "count": count} for event, count in conversion_stats
                ],
                "averages": {
                    "messages_per_session": (
                        round(float(avg_messages), 2) if avg_messages is not None else 0
                    ),
                    "session_duration_seconds": (
                        round(float(avg_duration), 2) if avg_duration is not None else 0
                    ),
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/intents", methods=["GET"])
def get_intent_analytics():
    """Pobierz analitykę intencji"""
    try:
        days = request.args.get("days", 7, type=int)
        start_date = (datetime.now(timezone.utc) - timedelta(days=days)).date()

        # Agregacja według intencji
        intent_summary = (
            db.session.query(
                IntentAnalytics.intent_name,
                func.sum(IntentAnalytics.trigger_count).label("total_triggers"),
                func.sum(IntentAnalytics.success_count).label("total_success"),
                func.sum(IntentAnalytics.failure_count).label("total_failures"),
                func.avg(IntentAnalytics.avg_confidence).label("avg_confidence"),
            )
            .filter(IntentAnalytics.date >= start_date)
            .group_by(IntentAnalytics.intent_name)
            .order_by(func.sum(IntentAnalytics.trigger_count).desc())
            .limit(10)
            .all()
        )

        return jsonify(
            {
                "status": "success",
                "intent_summary": [
                    {
                        "intent": intent,
                        "triggers": triggers,
                        "success": success,
                        "failures": failures,
                        "success_rate": round((success / triggers * 100) if triggers > 0 else 0, 2),
                        "avg_confidence": round(confidence, 2) if confidence else 0,
                    }
                    for intent, triggers, success, failures, confidence in intent_summary
                ],
                "total_intents": len(intent_summary),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/performance", methods=["GET"])
def get_performance_metrics():
    """Pobierz metryki wydajności"""
    try:
        hours = request.args.get("hours", 24, type=int)
        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        # Metryki wydajności
        metrics = PerformanceMetrics.query.filter(PerformanceMetrics.timestamp >= start_time).all()

        # Statystyki według endpointu
        from sqlalchemy import case

        endpoint_stats = (
            db.session.query(
                PerformanceMetrics.endpoint,
                func.count(PerformanceMetrics.id).label("request_count"),
                func.avg(PerformanceMetrics.response_time_ms).label("avg_response_time"),
                func.max(PerformanceMetrics.response_time_ms).label("max_response_time"),
                func.sum(case((PerformanceMetrics.status_code >= 400, 1), else_=0)).label(
                    "error_count"
                ),
            )
            .filter(PerformanceMetrics.timestamp >= start_time)
            .group_by(PerformanceMetrics.endpoint)
            .all()
        )

        # Średnie zużycie zasobów
        avg_memory = (
            db.session.query(func.avg(PerformanceMetrics.memory_usage_mb))
            .filter(
                PerformanceMetrics.timestamp >= start_time,
                PerformanceMetrics.memory_usage_mb.isnot(None),
            )
            .scalar()
        )

        avg_cpu = (
            db.session.query(func.avg(PerformanceMetrics.cpu_usage_percent))
            .filter(
                PerformanceMetrics.timestamp >= start_time,
                PerformanceMetrics.cpu_usage_percent.isnot(None),
            )
            .scalar()
        )

        return jsonify(
            {
                "status": "success",
                "period_hours": hours,
                "endpoint_performance": [
                    {
                        "endpoint": endpoint,
                        "request_count": count,
                        "avg_response_time_ms": round(avg_time, 2) if avg_time else 0,
                        "max_response_time_ms": max_time,
                        "error_count": errors,
                        "error_rate": round((errors / count * 100) if count > 0 else 0, 2),
                    }
                    for endpoint, count, avg_time, max_time, errors in endpoint_stats
                ],
                "resource_usage": {
                    "avg_memory_mb": round(avg_memory, 2) if avg_memory else 0,
                    "avg_cpu_percent": round(avg_cpu, 2) if avg_cpu else 0,
                },
                "total_requests": len(metrics),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/leads", methods=["GET"])
def get_lead_analytics():
    """Pobierz analitykę leadów"""
    try:
        days = _clamp_days(request.args.get("days", 7, type=int))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Leady według dnia
        leads_by_day = (
            db.session.query(
                func.date(Lead.created_at).label("date"), func.count(Lead.id).label("count")
            )
            .filter(Lead.created_at >= start_date)
            .group_by(func.date(Lead.created_at))
            .order_by(func.date(Lead.created_at))
            .all()
        )

        # Leady według pakietu
        leads_by_package = (
            db.session.query(Lead.interested_package, func.count(Lead.id).label("count"))
            .filter(Lead.created_at >= start_date, Lead.interested_package.isnot(None))
            .group_by(Lead.interested_package)
            .all()
        )

        # Leady według typu nieruchomości
        leads_by_property = (
            db.session.query(Lead.property_type, func.count(Lead.id).label("count"))
            .filter(Lead.created_at >= start_date, Lead.property_type.isnot(None))
            .group_by(Lead.property_type)
            .all()
        )

        total_leads = Lead.query.filter(Lead.created_at >= start_date).count()

        return jsonify(
            {
                "status": "success",
                "total_leads": total_leads,
                "leads_by_day": [
                    {"date": str(date), "count": count} for date, count in leads_by_day
                ],
                "leads_by_package": [
                    {"package": package, "count": count} for package, count in leads_by_package
                ],
                "leads_by_property_type": [
                    {"property_type": prop_type, "count": count}
                    for prop_type, count in leads_by_property
                ],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/export", methods=["GET"])
def export_analytics():
    """Eksportuj dane analityczne"""
    try:
        export_type = request.args.get("type", "overview")
        days = _clamp_days(request.args.get("days", 30, type=int), default=30, max_days=60)
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        data = {}

        if export_type == "overview" or export_type == "all":
            # Eksport przeglądu
            conversations = Conversation.query.filter(Conversation.timestamp >= start_date).all()
            data["conversations"] = [conv.to_dict() for conv in conversations]

        if export_type == "leads" or export_type == "all":
            # Eksport leadów
            leads = Lead.query.filter(Lead.created_at >= start_date).all()
            data["leads"] = [lead.to_dict() for lead in leads]

        if export_type == "engagement" or export_type == "all":
            # Eksport zaangażowania
            engagements = UserEngagement.query.filter(
                UserEngagement.first_interaction >= start_date
            ).all()
            data["engagements"] = [eng.to_dict() for eng in engagements]

        return jsonify(
            {
                "status": "success",
                "export_type": export_type,
                "period_days": days,
                "data": data,
                "exported_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/dashboard/summary", methods=["GET"])
def dashboard_summary():
    """Dashboard summary - legacy endpoint for compatibility"""
    try:
        days = _clamp_days(request.args.get("days", 30, type=int), default=30, max_days=60)
        # budget = request.args.get("budget", 0, type=int)  # For future use

        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Get all analytics
        conversations_count = Conversation.query.filter(
            Conversation.timestamp >= start_date
        ).count()

        leads_count = Lead.query.filter(Lead.created_at >= start_date).count()

        intents = IntentAnalytics.query.filter(IntentAnalytics.date >= start_date.date()).all()

        top_intent = "unknown"
        if intents:
            top_intent = max(
                ((i.intent_name, i.success_count) for i in intents), key=lambda x: x[1]
            )
            top_intent_name, top_intent_count = top_intent
        else:
            top_intent_name = "unknown"
            top_intent_count = 0

        # Calculate conversion
        conversion_rate = (
            (leads_count / conversations_count * 100) if conversations_count > 0 else 0
        )

        return (
            jsonify(
                {
                    "period_days": days,
                    "conversations": conversations_count,
                    "leads": leads_count,
                    "conversion_rate": round(conversion_rate, 1),
                    "top_intent": {"name": top_intent_name, "count": top_intent_count},
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# ========================================
# ADVANCED ANALYTICS ENDPOINTS
# ========================================


@analytics_bp.route("/advanced/sentiment", methods=["POST"])
def analyze_sentiment():
    """
    Analyze sentiment of a message
    POST /api/analytics/advanced/sentiment
    Body: {"message": "text to analyze"}
    """
    try:
        from src.services.analytics_service import AdvancedAnalytics

        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "Message is required"}), 400

        result = AdvancedAnalytics.analyze_sentiment(message)

        return jsonify({"status": "success", "message": message, "sentiment_analysis": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/advanced/heatmap", methods=["GET"])
def get_activity_heatmap():
    """
    Get activity heatmap (hour x day of week)
    GET /api/analytics/advanced/heatmap?days=30
    """
    try:
        from src.services.analytics_service import AdvancedAnalytics

        days = request.args.get("days", 30, type=int)
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)

        result = AdvancedAnalytics.get_activity_heatmap(start_date, end_date)

        return (
            jsonify(
                {
                    "status": "success",
                    "period": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat(),
                        "days": days,
                    },
                    "heatmap_data": result,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/advanced/funnel", methods=["GET"])
def get_conversion_funnel():
    """
    Get conversion funnel analysis
    GET /api/analytics/advanced/funnel?days=30
    """
    try:
        from src.services.analytics_service import AdvancedAnalytics

        days = request.args.get("days", 30, type=int)
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)

        result = AdvancedAnalytics.get_conversion_funnel(start_date, end_date)

        return (
            jsonify(
                {
                    "status": "success",
                    "period": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat(),
                        "days": days,
                    },
                    "funnel_data": result,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/advanced/cohort", methods=["GET"])
def get_cohort_analysis():
    """
    Get cohort retention analysis
    GET /api/analytics/advanced/cohort?period=week&num_cohorts=8
    """
    try:
        from src.services.analytics_service import AdvancedAnalytics

        period = request.args.get("period", "week")  # day/week/month
        num_cohorts = request.args.get("num_cohorts", 8, type=int)

        if period not in ["day", "week", "month"]:
            return jsonify({"error": "Period must be day, week, or month"}), 400

        result = AdvancedAnalytics.get_cohort_analysis(period, num_cohorts)

        return jsonify({"status": "success", "cohort_data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/advanced/journey/<session_id>", methods=["GET"])
def get_user_journey(session_id):
    """
    Get detailed user journey for a specific session
    GET /api/analytics/advanced/journey/{session_id}
    """
    try:
        from src.services.analytics_service import AdvancedAnalytics

        result = AdvancedAnalytics.get_user_journey_insights(session_id)

        if "error" in result:
            return jsonify({"status": "error", "error": result["error"]}), 404

        return jsonify({"status": "success", "journey_data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# ===== ADVANCED ANALYTICS ENDPOINTS (v2.5) =====


@analytics_bp.route("/v2/funnel", methods=["GET"])
def get_funnel_v2():
    """Get conversion funnel analysis (v2)"""
    try:
        from src.services.advanced_analytics import advanced_analytics

        result = advanced_analytics.get_conversion_funnel()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route("/v2/trends", methods=["GET"])
def get_trends_v2():
    """Get weekly trends (v2)"""
    try:
        from src.services.advanced_analytics import advanced_analytics

        weeks = request.args.get("weeks", 4, type=int)
        result = advanced_analytics.get_weekly_trends(weeks=weeks)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route("/v2/intents", methods=["GET"])
def get_intents_v2():
    """Get intent distribution analysis (v2)"""
    try:
        from src.services.advanced_analytics import advanced_analytics

        result = advanced_analytics.get_intent_distribution()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route("/v2/export/csv", methods=["GET"])
def export_csv_v2():
    """Export analytics data to CSV (v2)"""
    try:
        from flask import make_response

        from src.services.advanced_analytics import advanced_analytics

        data_type = request.args.get("type", "leads")
        filters = {
            "status": request.args.get("status"),
            "min_score": request.args.get("min_score", type=int),
        }

        csv_data = advanced_analytics.export_to_csv(data_type, filters)

        response = make_response(csv_data)
        response.headers["Content-Type"] = "text/csv"
        response.headers["Content-Disposition"] = f"attachment; filename={data_type}_export.csv"

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
