"""
FollowupEvent model for idempotent follow-up message delivery.

IDEMPOTENCY PATTERN:
- Before sending follow-up: INSERT INTO followup_events (conversation_id, followup_number)
- If IntegrityError (duplicate): Skip sending (already sent)
- If success: Send message + commit transaction
- Prevents duplicate messages on retries/restarts/crashes

DATABASE CONSTRAINT:
- UNIQUE(conversation_id, followup_number) ensures each follow-up sent exactly once
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

from src.models.chatbot import db


class FollowupEvent(db.Model):
    """
    Tracks follow-up message delivery for idempotency.

    UNIQUE constraint on (conversation_id, followup_number) prevents duplicate sends.
    """

    __tablename__ = "followup_events"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, nullable=False, index=True)
    followup_number = Column(Integer, nullable=False)  # 1, 2, 3, etc.

    sent_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = Column(String(20), nullable=False, default="sent")  # sent, failed, cancelled

    # Idempotency constraint: each follow-up sent only once per conversation
    __table_args__ = (
        UniqueConstraint("conversation_id", "followup_number", name="uq_conversation_followup"),
    )

    def __repr__(self):
        return f"<FollowupEvent conv={self.conversation_id} #={self.followup_number} at={self.sent_at}>"
