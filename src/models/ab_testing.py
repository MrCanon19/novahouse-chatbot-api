"""
A/B Testing Models
==================
Database models for A/B testing experiments
"""

from datetime import datetime, timezone
from src.models.chatbot import db
import json

class Experiment(db.Model):
    """A/B test experiment model"""
    __tablename__ = 'experiments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Experiment configuration
    experiment_type = db.Column(db.String(50), nullable=False)  # prompt, greeting, cta, etc.
    status = db.Column(db.String(20), default='draft')  # draft, active, paused, completed
    
    # Variants (JSON)
    variants = db.Column(db.Text, nullable=False)  # [{"id": "A", "name": "Control", "content": "..."}, {"id": "B", ...}]
    
    # Traffic allocation
    traffic_allocation = db.Column(db.Float, default=1.0)  # 0.0-1.0 (percentage of users in experiment)
    
    # Success metrics
    primary_metric = db.Column(db.String(50))  # conversion_rate, engagement, satisfaction
    goal_threshold = db.Column(db.Float)  # Target metric value
    
    # Statistical significance
    confidence_level = db.Column(db.Float, default=0.95)  # 95% confidence
    min_sample_size = db.Column(db.Integer, default=100)  # Minimum participants per variant
    
    # Timing
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Winner
    winner_variant_id = db.Column(db.String(10))
    winner_declared_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'experiment_type': self.experiment_type,
            'status': self.status,
            'variants': json.loads(self.variants) if self.variants else [],
            'traffic_allocation': self.traffic_allocation,
            'primary_metric': self.primary_metric,
            'goal_threshold': self.goal_threshold,
            'confidence_level': self.confidence_level,
            'min_sample_size': self.min_sample_size,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat(),
            'winner_variant_id': self.winner_variant_id,
            'winner_declared_at': self.winner_declared_at.isoformat() if self.winner_declared_at else None
        }

class ExperimentParticipant(db.Model):
    """Tracks which users see which variant"""
    __tablename__ = 'experiment_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.String(100), default='anonymous')
    
    # Variant assignment
    variant_id = db.Column(db.String(10), nullable=False)  # A, B, C, etc.
    
    # Participation timestamp
    assigned_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Results
    converted = db.Column(db.Boolean, default=False)
    conversion_value = db.Column(db.Float)  # Optional: revenue, score, etc.
    engaged = db.Column(db.Boolean, default=False)  # Sent 3+ messages
    satisfied = db.Column(db.Boolean)  # Positive sentiment
    
    # Interaction metrics
    messages_sent = db.Column(db.Integer, default=0)
    session_duration = db.Column(db.Integer)  # seconds
    
    def to_dict(self):
        return {
            'id': self.id,
            'experiment_id': self.experiment_id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'variant_id': self.variant_id,
            'assigned_at': self.assigned_at.isoformat(),
            'converted': self.converted,
            'conversion_value': self.conversion_value,
            'engaged': self.engaged,
            'satisfied': self.satisfied,
            'messages_sent': self.messages_sent,
            'session_duration': self.session_duration
        }

class ExperimentResult(db.Model):
    """Aggregated results for each variant"""
    __tablename__ = 'experiment_results'
    
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)
    variant_id = db.Column(db.String(10), nullable=False)
    
    # Participant counts
    total_participants = db.Column(db.Integer, default=0)
    total_conversions = db.Column(db.Integer, default=0)
    total_engaged = db.Column(db.Integer, default=0)
    
    # Metrics
    conversion_rate = db.Column(db.Float, default=0.0)
    engagement_rate = db.Column(db.Float, default=0.0)
    avg_session_duration = db.Column(db.Float)
    avg_messages = db.Column(db.Float)
    satisfaction_rate = db.Column(db.Float)
    
    # Statistical significance
    is_statistically_significant = db.Column(db.Boolean, default=False)
    p_value = db.Column(db.Float)
    confidence_interval_lower = db.Column(db.Float)
    confidence_interval_upper = db.Column(db.Float)
    
    # Timestamps
    calculated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'experiment_id': self.experiment_id,
            'variant_id': self.variant_id,
            'total_participants': self.total_participants,
            'total_conversions': self.total_conversions,
            'total_engaged': self.total_engaged,
            'conversion_rate': round(self.conversion_rate, 4) if self.conversion_rate else 0,
            'engagement_rate': round(self.engagement_rate, 4) if self.engagement_rate else 0,
            'avg_session_duration': round(self.avg_session_duration, 2) if self.avg_session_duration else 0,
            'avg_messages': round(self.avg_messages, 2) if self.avg_messages else 0,
            'satisfaction_rate': round(self.satisfaction_rate, 4) if self.satisfaction_rate else 0,
            'is_statistically_significant': self.is_statistically_significant,
            'p_value': round(self.p_value, 6) if self.p_value else None,
            'confidence_interval': {
                'lower': round(self.confidence_interval_lower, 4) if self.confidence_interval_lower else None,
                'upper': round(self.confidence_interval_upper, 4) if self.confidence_interval_upper else None
            },
            'calculated_at': self.calculated_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
