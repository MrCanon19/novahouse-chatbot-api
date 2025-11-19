import json
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Intent(db.Model):
    """Model dla intencji chatbota"""

    __tablename__ = "intents"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    training_phrases = db.Column(db.Text, nullable=False)  # JSON string
    response_templates = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "training_phrases": json.loads(self.training_phrases),
            "response_templates": json.loads(self.response_templates),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Entity(db.Model):
    """Model dla encji chatbota"""

    __tablename__ = "entities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    values = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "values": json.loads(self.values),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Conversation(db.Model):
    """Model dla konwersacji z chatbotem"""

    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(100))
    entities = db.Column(db.Text)  # JSON string
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_message": self.user_message,
            "bot_response": self.bot_response,
            "intent": self.intent,
            "entities": json.loads(self.entities) if self.entities else {},
            "timestamp": self.timestamp.isoformat(),
        }


class Lead(db.Model):
    """Model dla leadów z chatbota"""

    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    interested_package = db.Column(db.String(50))
    property_size = db.Column(db.String(20))
    property_type = db.Column(db.String(50))
    location = db.Column(db.String(100))
    additional_info = db.Column(db.Text)
    message = db.Column(db.Text)
    source = db.Column(db.String(50), default="chatbot")
    status = db.Column(db.String(50), default="new")
    notes = db.Column(db.Text)
    monday_item_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "interested_package": self.interested_package,
            "property_size": self.property_size,
            "property_type": self.property_type,
            "location": self.location,
            "additional_info": self.additional_info,
            "message": self.message,
            "source": self.source,
            "status": self.status,
            "notes": self.notes,
            "monday_item_id": self.monday_item_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ChatConversation(db.Model):
    """Model for chat conversation sessions"""

    __tablename__ = "chat_conversations"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    started_at = db.Column(db.DateTime, nullable=False)
    ended_at = db.Column(db.DateTime)
    context_data = db.Column(db.Text)  # JSON: {name, email, city, square_meters, package}

    messages = db.relationship(
        "ChatMessage", backref="conversation", lazy=True, cascade="all, delete-orphan"
    )


class ChatMessage(db.Model):
    """Model for individual chat messages"""

    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("chat_conversations.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(20), nullable=False)  # 'user' or 'bot'
    timestamp = db.Column(db.DateTime, nullable=False)


class RodoConsent(db.Model):
    """Model for RODO/GDPR consent tracking"""

    __tablename__ = "rodo_consents"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    consent_given = db.Column(db.Boolean, default=False, nullable=False)
    consent_date = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "consent_given": self.consent_given,
            "consent_date": self.consent_date.isoformat() if self.consent_date else None,
            "ip_address": self.ip_address,
        }


class AuditLog(db.Model):
    """Simple audit log for admin actions (exports, deletions)."""

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)  # e.g. 'export', 'delete'
    session_id = db.Column(db.String(100))
    admin_user = db.Column(db.String(100))
    ip_address = db.Column(db.String(50))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action,
            "session_id": self.session_id,
            "admin_user": self.admin_user,
            "ip_address": self.ip_address,
            "details": self.details,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
