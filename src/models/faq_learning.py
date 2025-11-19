"""
FAQ Learning System Models
===========================
Track unanswered questions and learn from them
"""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UnknownQuestion(db.Model):
    """Log questions that bot couldn't answer well"""

    __tablename__ = "unknown_questions"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    question = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text)
    was_helpful = db.Column(db.Boolean)  # User feedback
    user_feedback = db.Column(db.Text)  # Optional user comment
    category = db.Column(db.String(50))  # Auto-categorized
    status = db.Column(db.String(20), default="pending")  # pending, reviewed, added_to_faq, ignored
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "question": self.question,
            "bot_response": self.bot_response,
            "was_helpful": self.was_helpful,
            "user_feedback": self.user_feedback,
            "category": self.category,
            "status": self.status,
            "admin_notes": self.admin_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "reviewed_by": self.reviewed_by,
        }


class LearnedFAQ(db.Model):
    """New FAQ entries learned from user questions"""

    __tablename__ = "learned_faq"

    id = db.Column(db.Integer, primary_key=True)
    question_pattern = db.Column(db.String(200), nullable=False)  # Keywords to match
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    usage_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "question_pattern": self.question_pattern,
            "answer": self.answer,
            "category": self.category,
            "usage_count": self.usage_count,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
