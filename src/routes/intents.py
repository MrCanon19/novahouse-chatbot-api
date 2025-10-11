"""
Intent management endpoints
"""
from flask import Blueprint, request, jsonify
from src.models.chatbot import db, Intent
import json

intents_bp = Blueprint('intents', __name__)

@intents_bp.route('/', methods=['GET'])
def get_intents():
    """Pobierz listę wszystkich intencji"""
    try:
        intents = Intent.query.all()
        
        return jsonify({
            'success': True,
            'count': len(intents),
            'intents': [
                {
                    'id': intent.id,
                    'name': intent.name,
                    'training_phrases_count': len(json.loads(intent.training_phrases)) if intent.training_phrases else 0,
                    'created_at': intent.created_at.isoformat() if intent.created_at else None
                }
                for intent in intents
            ]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intents_bp.route('/<int:intent_id>', methods=['GET'])
def get_intent(intent_id):
    """Pobierz szczegóły intencji"""
    try:
        intent = Intent.query.get(intent_id)
        
        if not intent:
            return jsonify({
                'success': False,
                'error': 'Intent not found'
            }), 404
        
        return jsonify({
            'success': True,
            'intent': intent.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500