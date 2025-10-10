from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Intent(db.Model):
    """Model dla intencji chatbota"""
    __tablename__ = 'intents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    training_phrases = db.Column(db.Text, nullable=False)  # JSON string
    response_templates = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'training_phrases': json.loads(self.training_phrases),
            'response_templates': json.loads(self.response_templates),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Entity(db.Model):
    """Model dla encji chatbota"""
    __tablename__ = 'entities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    values = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'values': json.loads(self.values),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Conversation(db.Model):
    """Model dla konwersacji z chatbotem"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(100))
    entities = db.Column(db.Text)  # JSON string
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'intent': self.intent,
            'entities': json.loads(self.entities) if self.entities else {},
            'timestamp': self.timestamp.isoformat()
        }

class Lead(db.Model):
    """Model dla leadów z chatbota"""
    __tablename__ = 'leads'
    
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'interested_package': self.interested_package,
            'property_size': self.property_size,
            'property_type': self.property_type,
            'location': self.location,
            'additional_info': self.additional_info,
            'created_at': self.created_at.isoformat()
        }

