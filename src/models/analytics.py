from datetime import datetime, timezone
import json
from src.models.chatbot import db


class ChatAnalytics(db.Model):
    """Model dla analityki konwersacji chatbota"""

    __tablename__ = "chat_analytics"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.String(100), default="anonymous")
    message_count = db.Column(db.Integer, default=0)
    intent_detected = db.Column(db.String(100))
    entities_extracted = db.Column(db.Text)  # JSON string
    sentiment = db.Column(db.String(20))  # positive, negative, neutral
    response_time_ms = db.Column(db.Integer)
    user_satisfied = db.Column(db.Boolean)
    lead_generated = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "message_count": self.message_count,
            "intent_detected": self.intent_detected,
            "entities_extracted": (
                json.loads(self.entities_extracted) if self.entities_extracted else {}
            ),
            "sentiment": self.sentiment,
            "response_time_ms": self.response_time_ms,
            "user_satisfied": self.user_satisfied,
            "lead_generated": self.lead_generated,
            "timestamp": self.timestamp.isoformat(),
        }


class UserEngagement(db.Model):
    """Model dla zaangażowania użytkowników"""

    __tablename__ = "user_engagement"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, unique=True, index=True)
    user_id = db.Column(db.String(100), default="anonymous")
    first_interaction = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_interaction = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    total_messages = db.Column(db.Integer, default=0)
    session_duration_seconds = db.Column(db.Integer)
    pages_visited = db.Column(db.Text)  # JSON array
    conversion_event = db.Column(db.String(100))  # lead_form, contact_request, etc.
    device_type = db.Column(db.String(50))  # mobile, desktop, tablet
    browser = db.Column(db.String(50))
    referrer = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "first_interaction": self.first_interaction.isoformat(),
            "last_interaction": self.last_interaction.isoformat(),
            "total_messages": self.total_messages,
            "session_duration_seconds": self.session_duration_seconds,
            "pages_visited": json.loads(self.pages_visited) if self.pages_visited else [],
            "conversion_event": self.conversion_event,
            "device_type": self.device_type,
            "browser": self.browser,
            "referrer": self.referrer,
        }


class IntentAnalytics(db.Model):
    """Model dla analityki intencji"""

    __tablename__ = "intent_analytics"

    id = db.Column(db.Integer, primary_key=True)
    intent_name = db.Column(db.String(100), nullable=False, index=True)
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date(), index=True)
    trigger_count = db.Column(db.Integer, default=0)
    success_count = db.Column(db.Integer, default=0)
    failure_count = db.Column(db.Integer, default=0)
    avg_confidence = db.Column(db.Float)
    avg_response_time_ms = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "intent_name": self.intent_name,
            "date": self.date.isoformat(),
            "trigger_count": self.trigger_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "avg_confidence": self.avg_confidence,
            "avg_response_time_ms": self.avg_response_time_ms,
        }


class PerformanceMetrics(db.Model):
    """Model dla metryk wydajności systemu"""

    __tablename__ = "performance_metrics"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    endpoint = db.Column(db.String(100), nullable=False)
    response_time_ms = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    memory_usage_mb = db.Column(db.Float)
    cpu_usage_percent = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "endpoint": self.endpoint,
            "response_time_ms": self.response_time_ms,
            "status_code": self.status_code,
            "error_message": self.error_message,
            "memory_usage_mb": self.memory_usage_mb,
            "cpu_usage_percent": self.cpu_usage_percent,
        }
