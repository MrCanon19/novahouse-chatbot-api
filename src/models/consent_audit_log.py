"""
ConsentAuditLog model for tracking RODO and marketing consent changes.

AUDIT TRAIL: Every unsubscribe/opt-out action is logged with:
- User IP address (for security)
- Timestamp (for compliance)
- Action type (unsubscribe, revoke-consent, etc.)
- Conversation/Lead ID (for association)

Required for GDPR/RODO compliance and customer support audits.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from src.models.chatbot import db


class ConsentAuditLog(db.Model):
    """
    Audit log for all RODO/consent changes.
    Required for compliance and customer support.
    """

    __tablename__ = "consent_audit_log"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, index=True)  # NULL if lead-based
    lead_id = Column(Integer, index=True)  # NULL if conversation-based

    email = Column(String(255), index=True)  # Store email for unsubscribe tracking
    action = Column(String(50), nullable=False)  # 'unsubscribe', 'revoke-consent', 'opt-in', etc.

    timestamp = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True
    )
    ip_address = Column(String(50))  # For security audit
    user_agent = Column(Text)  # For security audit

    reason = Column(Text)  # Optional reason from user
    notes = Column(Text)  # Admin notes

    def __repr__(self):
        return f"<ConsentAuditLog action={self.action} email={self.email} at={self.timestamp}>"
