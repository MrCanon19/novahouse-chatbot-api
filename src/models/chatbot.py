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
    # Enhanced fields
    lead_score = db.Column(db.Integer, default=0)  # 0-100 scoring
    conversation_summary = db.Column(db.Text)  # AI-generated summary
    data_confirmed = db.Column(db.Boolean, default=False)  # User confirmed data
    last_interaction = db.Column(db.DateTime)  # For follow-up timing
    # Email verification fields
    email_verified = db.Column(db.Boolean, default=False)  # Email verified flag
    email_verification_token = db.Column(db.String(128))  # Email verification token
    email_verified_at = db.Column(db.DateTime)  # When email was verified
    # Phone verification fields
    phone_verified = db.Column(db.Boolean, default=False)  # Phone verified flag
    phone_verification_code = db.Column(db.String(6))  # 6-digit SMS code
    phone_verified_at = db.Column(db.DateTime)  # When phone was verified
    # Lead assignment fields
    assigned_to_user_id = db.Column(db.String(100))  # Sales person ID
    assigned_at = db.Column(db.DateTime)  # When assigned
    first_contact_at = db.Column(db.DateTime)  # First contact timestamp
    expected_contact_by = db.Column(db.DateTime)  # SLA deadline
    # RODO/GDPR Consent fields - removed from DB, using notes or separate table instead
    # marketing_consent = db.Column(db.Boolean, default=True)
    # rodo_consent = db.Column(db.Boolean, default=True)
    
    @property
    def marketing_consent(self):
        """Get marketing_consent from notes for backward compatibility"""
        if self.notes and "marketing_consent:true" in self.notes.lower():
            return True
        return True  # Default to True
    
    @marketing_consent.setter
    def marketing_consent(self, value):
        """Set marketing_consent in notes for backward compatibility"""
        if not self.notes:
            self.notes = ""
        if "marketing_consent:" not in self.notes:
            self.notes += f"\nmarketing_consent:{value}"
        else:
            import re
            self.notes = re.sub(r'marketing_consent:\w+', f'marketing_consent:{value}', self.notes)
    
    @property
    def rodo_consent(self):
        """Get rodo_consent from notes for backward compatibility"""
        if self.notes and "rodo_consent:true" in self.notes.lower():
            return True
        return True  # Default to True
    
    @rodo_consent.setter
    def rodo_consent(self, value):
        """Set rodo_consent in notes for backward compatibility"""
        if not self.notes:
            self.notes = ""
        if "rodo_consent:" not in self.notes:
            self.notes += f"\nrodo_consent:{value}"
        else:
            import re
            self.notes = re.sub(r'rodo_consent:\w+', f'rodo_consent:{value}', self.notes)  # Data processing consent
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


class Booking(db.Model):
    """Model dla rezerwacji spotkań (Zencal)"""

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"))
    session_id = db.Column(db.String(100))
    zencal_booking_id = db.Column(db.String(100))  # ID z Zencal
    zencal_link = db.Column(db.String(500))  # Link do rezerwacji
    client_name = db.Column(db.String(100))
    client_email = db.Column(db.String(100))
    client_phone = db.Column(db.String(20))
    appointment_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default="pending")  # pending, confirmed, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "session_id": self.session_id,
            "zencal_booking_id": self.zencal_booking_id,
            "zencal_link": self.zencal_link,
            "client_name": self.client_name,
            "client_email": self.client_email,
            "client_phone": self.client_phone,
            "appointment_date": (
                self.appointment_date.isoformat() if self.appointment_date else None
            ),
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class FollowUpTest(db.Model):
    """A/B Testing for follow-up questions"""

    __tablename__ = "followup_tests"

    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(100), nullable=False)  # e.g., "package_to_sqm"
    variant_a = db.Column(db.Text, nullable=False)  # Question variant A
    variant_b = db.Column(db.Text, nullable=False)  # Question variant B
    variant_a_shown = db.Column(db.Integer, default=0)
    variant_b_shown = db.Column(db.Integer, default=0)
    variant_a_responses = db.Column(db.Integer, default=0)  # User responded
    variant_b_responses = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        conv_rate_a = (
            (self.variant_a_responses / self.variant_a_shown * 100)
            if self.variant_a_shown > 0
            else 0
        )
        conv_rate_b = (
            (self.variant_b_responses / self.variant_b_shown * 100)
            if self.variant_b_shown > 0
            else 0
        )
        return {
            "id": self.id,
            "question_type": self.question_type,
            "variant_a": self.variant_a,
            "variant_b": self.variant_b,
            "stats": {
                "variant_a": {
                    "shown": self.variant_a_shown,
                    "responses": self.variant_a_responses,
                    "conversion_rate": round(conv_rate_a, 2),
                },
                "variant_b": {
                    "shown": self.variant_b_shown,
                    "responses": self.variant_b_responses,
                    "conversion_rate": round(conv_rate_b, 2),
                },
            },
            "is_active": self.is_active,
        }


class CompetitiveIntel(db.Model):
    """Track competitive intelligence from conversations"""

    __tablename__ = "competitive_intel"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    intel_type = db.Column(
        db.String(50), nullable=False
    )  # competitor_mention, price_comparison, feature_request
    competitor_name = db.Column(db.String(100))  # If mentioned
    user_message = db.Column(db.Text, nullable=False)  # Original message
    context = db.Column(db.Text)  # Additional context
    sentiment = db.Column(db.String(20))  # positive, negative, neutral
    priority = db.Column(db.String(20), default="medium")  # low, medium, high
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "intel_type": self.intel_type,
            "competitor_name": self.competitor_name,
            "user_message": self.user_message,
            "context": self.context,
            "sentiment": self.sentiment,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ChatConversation(db.Model):
    """Model for chat conversation sessions"""

    __tablename__ = "chat_conversations"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    # email column removed - using context_data instead to avoid migration issues
    # email = db.Column(db.String(255), nullable=True, index=True)
    started_at = db.Column(db.DateTime, nullable=False)
    ended_at = db.Column(db.DateTime)
    context_data = db.Column(db.Text)  # JSON: {name, email, city, square_meters, package}
    
    @property
    def email(self):
        """Get email from context_data for backward compatibility"""
        try:
            if self.context_data:
                context = json.loads(self.context_data)
                return context.get("email")
        except (json.JSONDecodeError, TypeError):
            pass
        return None
    
    @email.setter
    def email(self, value):
        """Set email in context_data for backward compatibility"""
        try:
            context = json.loads(self.context_data) if self.context_data else {}
            context["email"] = value
            self.context_data = json.dumps(context)
        except (json.JSONDecodeError, TypeError):
            self.context_data = json.dumps({"email": value})
    # Quality metrics
    user_satisfaction = db.Column(db.Integer)  # 1-5 rating
    feedback_text = db.Column(db.Text)  # Optional user feedback
    awaiting_confirmation = db.Column(db.Boolean, default=False)  # Pending data confirmation
    # A/B Testing
    followup_variant = db.Column(db.String(10))  # "A" or "B" for A/B test
    # V2.4 Improvements
    conversation_summary = db.Column(db.Text)  # AI-generated summary
    needs_human_review = db.Column(db.Boolean, default=False)  # Sentiment escalation
    followup_count = db.Column(db.Integer, default=0)  # Number of followups sent
    last_followup_at = db.Column(db.DateTime)  # Last followup timestamp
    # RODO/GDPR Consent fields - removed from DB, using context_data instead
    # marketing_consent = db.Column(db.Boolean, default=True)
    # rodo_consent = db.Column(db.Boolean, default=True)
    
    @property
    def marketing_consent(self):
        """Get marketing_consent from context_data for backward compatibility"""
        try:
            if self.context_data:
                context = json.loads(self.context_data)
                return context.get("marketing_consent", True)
        except (json.JSONDecodeError, TypeError):
            pass
        return True
    
    @marketing_consent.setter
    def marketing_consent(self, value):
        """Set marketing_consent in context_data for backward compatibility"""
        try:
            context = json.loads(self.context_data) if self.context_data else {}
            context["marketing_consent"] = value
            self.context_data = json.dumps(context)
        except (json.JSONDecodeError, TypeError):
            self.context_data = json.dumps({"marketing_consent": value})
    
    @property
    def rodo_consent(self):
        """Get rodo_consent from context_data for backward compatibility"""
        try:
            if self.context_data:
                context = json.loads(self.context_data)
                return context.get("rodo_consent", True)
        except (json.JSONDecodeError, TypeError):
            pass
        return True
    
    @rodo_consent.setter
    def rodo_consent(self, value):
        """Set rodo_consent in context_data for backward compatibility"""
        try:
            context = json.loads(self.context_data) if self.context_data else {}
            context["rodo_consent"] = value
            self.context_data = json.dumps(context)
        except (json.JSONDecodeError, TypeError):
            self.context_data = json.dumps({"rodo_consent": value})

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
    is_followup = db.Column(db.Boolean, default=False)  # Auto-followup message


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


class DeadLetterQueue(db.Model):
    """Dead-letter queue for failed alerts and notifications"""

    __tablename__ = "dead_letter_queue"

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # 'slack_alert', 'email', 'sms'
    target = db.Column(db.String(255), nullable=False)  # webhook URL, email, phone
    payload = db.Column(db.Text, nullable=False)  # JSON payload
    error_message = db.Column(db.Text)  # Error from failed attempt
    retry_count = db.Column(db.Integer, default=0)  # Number of retry attempts
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True
    )
    last_retry_at = db.Column(db.DateTime)  # Last attempted retry time
    status = db.Column(db.String(20), default="pending")  # 'pending', 'delivered', 'failed'

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "target": self.target,
            "payload": json.loads(self.payload) if self.payload else {},
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_retry_at": self.last_retry_at.isoformat() if self.last_retry_at else None,
            "status": self.status,
        }
