from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy import func, text

from src.models.analytics import ChatAnalytics, IntentAnalytics, PerformanceMetrics, UserEngagement
from src.models.chatbot import ChatConversation, Lead, db
from src.middleware.security import require_auth

analytics_bp = Blueprint("analytics", __name__)

# All analytics endpoints require authentication
analytics_bp.before_request(require_auth)


def _clamp_days(raw_days: int, default: int = 7, max_days: int = 31) -> int:
    """Sanitize days parameter to prevent heavy full-table scans."""
    if raw_days is None:
        return default
    return max(1, min(raw_days, max_days))


@analytics_bp.route("/overview", methods=["GET"])
def get_overview():
    """Pobierz ogólny przegląd analityki"""
    try:
        # Parametry zapytania
        days = _clamp_days(request.args.get("days", 7, type=int))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Short per-request timeout to prevent long-running analytics scans from killing workers
        try:
            db.session.execute(text("SET LOCAL statement_timeout TO 5000"))
        except Exception:
            db.session.rollback()

        # Statystyki leadów
        try:
            total_leads = Lead.query.filter(Lead.created_at >= start_date).count()
        except Exception:
            db.session.rollback()
            total_leads = 0

        # Unikalne sesje - dla małych zakresów (<= 3 dni) użyj count distinct
        # dla większych wykorzystaj tabelę UserEngagement (1 wiersz na sesję) aby uniknąć drogich distinctów
        if days <= 3:
            try:
                unique_sessions = (
                    db.session.query(func.count(func.distinct(ChatConversation.session_id)))
                    .filter(ChatConversation.timestamp >= start_date)
                    .scalar()
                )
                unique_sessions = int(unique_sessions or 0)
            except Exception:
                db.session.rollback()
                unique_sessions = 0
        else:
            try:
                unique_sessions = (
                    db.session.query(func.count(UserEngagement.id))
                    .filter(UserEngagement.first_interaction >= start_date)
                    .scalar()
                )
                unique_sessions = int(unique_sessions or 0)
            except Exception:
                db.session.rollback()
                unique_sessions = 0

        # Statystyki konwersacji
        if days <= 3:
            try:
                total_conversations = (
                    db.session.query(func.count(ChatConversation.id))
                    .filter(ChatConversation.timestamp >= start_date)
                    .scalar()
                )
                total_conversations = int(total_conversations or 0)
            except Exception:
                db.session.rollback()
                total_conversations = 0
        else:
            # Szybkie przybliżenie: średnia liczba wiadomości na sesję * liczba sesji
            try:
                avg_messages_per_session = (
                    db.session.query(func.avg(UserEngagement.total_messages))
                    .filter(UserEngagement.first_interaction >= start_date)
                    .scalar()
                )
                avg_messages_per_session = (
                    float(avg_messages_per_session) if avg_messages_per_session else 5.0
                )
                total_conversations = int(unique_sessions * avg_messages_per_session)
            except Exception:
                db.session.rollback()
                total_conversations = int(unique_sessions * 5)

        # Średni czas trwania sesji
        avg_session_duration = (
            db.session.query(func.avg(UserEngagement.session_duration_seconds))
            .filter(UserEngagement.first_interaction >= start_date)
            .scalar()
        )
        avg_session_duration = (
            float(avg_session_duration) if avg_session_duration is not None else 0.0
        )

        # Współczynnik konwersji
        conversion_rate = (total_leads / unique_sessions * 100) if unique_sessions > 0 else 0

        # Top intencje
        top_intents = (
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

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/conversations", methods=["GET"])
def get_conversation_analytics():
    """Pobierz analitykę konwersacji"""
    try:
        days = _clamp_days(request.args.get("days", 7, type=int))
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Konwersacje według dnia
        conversations_by_day = (
            db.session.query(
                func.date(ChatConversation.timestamp).label("date"),
                func.count(ChatConversation.id).label("count"),
            )
            .filter(ChatConversation.timestamp >= start_date)
            .group_by(func.date(ChatConversation.timestamp))
            .order_by(func.date(ChatConversation.timestamp))
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

        # Set query timeout to prevent OOM from large table scans
        try:
            db.session.execute(text("SET LOCAL statement_timeout TO 3000"))
        except Exception:
            db.session.rollback()

        # Leady według dnia
        leads_by_day = (
            db.session.query(
                func.date(Lead.created_at).label("date"), func.count(Lead.id).label("count")
            )
            .filter(Lead.created_at >= start_date)
            .group_by(func.date(Lead.created_at))
            .order_by(func.date(Lead.created_at))
            .limit(366)  # Max 366 days, safety limit
            .all()
        )

        # Leady według pakietu
        leads_by_package = (
            db.session.query(Lead.interested_package, func.count(Lead.id).label("count"))
            .filter(Lead.created_at >= start_date, Lead.interested_package.isnot(None))
            .group_by(Lead.interested_package)
            .limit(100)  # Max 100 unique packages, safety limit
            .all()
        )

        # Leady według typu nieruchomości
        leads_by_property = (
            db.session.query(Lead.property_type, func.count(Lead.id).label("count"))
            .filter(Lead.created_at >= start_date, Lead.property_type.isnot(None))
            .group_by(Lead.property_type)
            .limit(100)  # Max 100 unique property types, safety limit
            .all()
        )

        # Leady według miasta (location)
        leads_by_city = (
            db.session.query(Lead.location, func.count(Lead.id).label("count"))
            .filter(Lead.created_at >= start_date, Lead.location.isnot(None))
            .group_by(Lead.location)
            .order_by(func.count(Lead.id).desc())
            .limit(50)  # Max 50 unique cities, safety limit
            .all()
        )

        # Conversion rate per city
        city_conversion = []
        for city, lead_count in leads_by_city:
            # Count conversations for this city (from context_data)
            city_conversations = (
                db.session.query(func.count(ChatConversation.id))
                .filter(
                    ChatConversation.timestamp >= start_date,
                    ChatConversation.context_data.like(f'%"city": "{city}"%'),
                )
                .scalar()
            ) or 0
            conversion_rate = (
                (lead_count / city_conversations * 100) if city_conversations > 0 else 0
            )
            city_conversion.append(
                {
                    "city": city,
                    "leads": lead_count,
                    "conversations": city_conversations,
                    "conversion_rate": round(conversion_rate, 2),
                }
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
                "leads_by_city": [
                    {"city": city, "count": count} for city, count in leads_by_city
                ],
                "city_conversion_rates": city_conversion,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@analytics_bp.route("/export", methods=["GET"])
def export_analytics():
    """Eksportuj dane analityczne (JSON lub CSV)"""
    try:
        export_type = request.args.get("type", "overview")
        format_type = request.args.get("format", "json")  # json, csv, pdf
        days = _clamp_days(request.args.get("days", 30, type=int), default=30, max_days=60)
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        data = {}

        if export_type == "overview" or export_type == "all":
            # Eksport przeglądu
            conversations = ChatConversation.query.filter(ChatConversation.timestamp >= start_date).all()
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

        # CSV export
        if format_type == "csv":
            from flask import make_response
            import csv
            import io

            output = io.StringIO()
            writer = csv.writer(output)

            # Write headers
            if export_type == "leads" or export_type == "all":
                writer.writerow(
                    [
                        "ID",
                        "Session ID",
                        "Name",
                        "Email",
                        "Phone",
                        "Package",
                        "Property Size",
                        "Location",
                        "Created At",
                    ]
                )
                for lead in data.get("leads", []):
                    writer.writerow(
                        [
                            lead.get("id"),
                            lead.get("session_id"),
                            lead.get("name"),
                            lead.get("email"),
                            lead.get("phone"),
                            lead.get("interested_package"),
                            lead.get("property_size"),
                            lead.get("location"),
                            lead.get("created_at"),
                        ]
                    )

            response = make_response(output.getvalue())
            response.headers["Content-Type"] = "text/csv"
            response.headers["Content-Disposition"] = f"attachment; filename=analytics_{export_type}_{days}days.csv"
            return response

        # PDF export
        if format_type == "pdf":
            try:
                from flask import make_response
                from reportlab.lib.pagesizes import letter
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.lib import colors
                import io

                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                story = []
                styles = getSampleStyleSheet()

                # Title
                story.append(Paragraph(f"Analytics Report - {days} days", styles["Title"]))
                story.append(Spacer(1, 12))

                # Summary
                story.append(Paragraph("Summary", styles["Heading2"]))
                summary_data = [
                    ["Metric", "Value"],
                    ["Total Conversations", str(len(data.get("conversations", [])))],
                    ["Total Leads", str(len(data.get("leads", [])))],
                    ["Total Engagements", str(len(data.get("engagements", [])))],
                ]
                summary_table = Table(summary_data)
                summary_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, 0), 14),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]
                    )
                )
                story.append(summary_table)
                story.append(Spacer(1, 12))

                # Leads table
                if data.get("leads"):
                    story.append(Paragraph("Leads", styles["Heading2"]))
                    leads_data = [["Name", "Email", "Phone", "Package", "Location"]]
                    for lead in data["leads"][:50]:  # Limit to 50 for PDF
                        leads_data.append(
                            [
                                lead.get("name", ""),
                                lead.get("email", ""),
                                lead.get("phone", ""),
                                lead.get("interested_package", ""),
                                lead.get("location", ""),
                            ]
                        )
                    leads_table = Table(leads_data)
                    leads_table.setStyle(
                        TableStyle(
                            [
                                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                                ("FONTSIZE", (0, 0), (-1, 0), 10),
                                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                                ("FONTSIZE", (0, 1), (-1, -1), 8),
                            ]
                        )
                    )
                    story.append(leads_table)

                doc.build(story)
                buffer.seek(0)

                response = make_response(buffer.read())
                response.headers["Content-Type"] = "application/pdf"
                response.headers["Content-Disposition"] = f"attachment; filename=analytics_{export_type}_{days}days.pdf"
                return response

            except ImportError:
                return jsonify({"error": "reportlab library required for PDF export. Install: pip install reportlab"}), 500

        # Default: JSON export
        return jsonify(
            {
                "status": "success",
                "export_type": export_type,
                "format": format_type,
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
        conversations_count = ChatConversation.query.filter(
            ChatConversation.timestamp >= start_date
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
