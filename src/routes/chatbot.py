from flask import Blueprint, request, jsonify
from datetime import datetime
import json

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Chatbot endpoint - database disabled"""
    try:
        data = request.get_json()
        
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        user_id = data.get('user_id', 'anonymous')
        
        # Simple response logic
        if not message:
            response = "Proszę wpisać wiadomość."
        elif 'cześć' in message.lower() or 'witaj' in message.lower():
            response = "Witaj! 👋 Jestem chatbotem NovaHouse. Mogę pomóc Ci z informacjami o naszych pakietach wykończeniowych!"
        elif 'pakiet' in message.lower():
            response = "Oferujemy różne pakiety wykończeniowe! Mogę Cię połączyć z konsultantem, który pomoże wybrać najlepszy dla Ciebie."
        elif 'cena' in message.lower():
            response = "Ceny zależą od wybranego pakietu. Czy chcesz umówić się na konsultację?"
        else:
            response = f"Dziękuję za wiadomość! Chatbot NovaHouse jest tutaj aby pomóc. Możesz zapytać o pakiety, ceny lub konsultację."
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing request: {str(e)}',
            'status': 'error'
        }), 500

@chatbot_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'novahouse-chatbot',
        'database': 'disabled (readonly filesystem)',
        'timestamp': datetime.now().isoformat()
    })
