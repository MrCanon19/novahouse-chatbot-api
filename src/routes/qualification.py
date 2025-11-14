from flask import Blueprint, request, jsonify
from src.models.chatbot import db, Lead
from src.knowledge.novahouse_info import QUALIFICATION_QUESTIONS, PACKAGES
from datetime import datetime, timezone

qualification_bp = Blueprint('qualification', __name__)

def calculate_recommendation(answers):
    """Oblicz rekomendację pakietu na podstawie odpowiedzi"""
    scores = {'standard': 0, 'premium': 0, 'luxury': 0}
    total_weight = 0
    
    for answer in answers:
        question_id = answer.get('question_id')
        user_answer = str(answer.get('answer', '')).lower()
        
        question = next((q for q in QUALIFICATION_QUESTIONS if q['id'] == question_id), None)
        if not question:
            continue
        
        weight = question.get('weight', 1)
        total_weight += weight
        scoring = question.get('scoring', {})
        
        for key, value in scoring.items():
            if matches_answer(user_answer, key, question['type']):
                package = value.get('package')
                points = value.get('points', 0)
                scores[package] += points * weight
                break
    
    if total_weight == 0:
        return None
    
    recommended = max(scores, key=scores.get)
    confidence = (scores[recommended] / sum(scores.values()) * 100) if sum(scores.values()) > 0 else 0
    
    return {
        'recommended_package': recommended,
        'package_details': PACKAGES[recommended],
        'scores': scores,
        'confidence': round(confidence, 1)
    }

def matches_answer(user_answer, scoring_key, question_type):
    """Sprawdź czy odpowiedź pasuje do klucza"""
    scoring_key_lower = scoring_key.lower()
    
    if question_type == 'boolean':
        return user_answer in scoring_key_lower or scoring_key_lower in user_answer
    
    if question_type == 'choice':
        return scoring_key_lower in user_answer or user_answer in scoring_key_lower
    
    if question_type in ['number', 'range']:
        try:
            num = float(user_answer)
            if '-' in scoring_key:
                parts = scoring_key.replace('+', '').split('-')
                if len(parts) == 2:
                    min_val = float(parts[0])
                    max_val = float(parts[1]) if parts[1] else float('inf')
                    return min_val <= num <= max_val
            elif '+' in scoring_key:
                min_val = float(scoring_key.replace('+', ''))
                return num >= min_val
        except:
            return False
    
    return False

@qualification_bp.route('/questions', methods=['GET'])
def get_questions():
    """Pobierz wszystkie pytania kwalifikacyjne"""
    return jsonify({
        'questions': QUALIFICATION_QUESTIONS,
        'total': len(QUALIFICATION_QUESTIONS)
    }), 200

@qualification_bp.route('/submit', methods=['POST'])
def submit_qualification():
    """Prześlij odpowiedzi i otrzymaj rekomendację"""
    data = request.get_json()
    
    if not data or 'answers' not in data:
        return jsonify({'error': 'Answers are required'}), 400
    
    answers = data['answers']
    contact_info = data.get('contact_info', {})
    qualification_data = data.get('qualification_data', {})
    
    recommendation = calculate_recommendation(answers)
    
    if not recommendation:
        return jsonify({'error': 'Could not calculate recommendation'}), 400
    
    # Zapisz jako lead jeśli są dane kontaktowe
    lead_id = None
    if contact_info.get('name') and contact_info.get('email'):
        try:
            lead = Lead(
                name=contact_info['name'],
                email=contact_info['email'],
                phone=contact_info.get('phone'),
                message=f"Kwalifikacja: {recommendation['recommended_package']} ({recommendation['confidence']}% pewności)",
                status='qualified',
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(lead)
            db.session.commit()
            lead_id = lead.id
            
            # Sync z Monday.com - z danymi kwalifikacji
            try:
                from src.integrations.monday_client import MondayClient
                monday = MondayClient()
                
                # Przygotuj dane dla Monday z kwalifikacją
                monday_lead_data = {
                    'name': lead.name,
                    'email': lead.email,
                    'phone': lead.phone,
                    'message': lead.message,
                    'recommended_package': recommendation['recommended_package'],
                    'confidence_score': recommendation['confidence'],
                    'property_type': qualification_data.get('property_type'),
                    'budget': qualification_data.get('budget'),
                    'interior_style': qualification_data.get('interior_style'),
                }
                
                monday_item_id = monday.create_lead_item(monday_lead_data)
                
                if monday_item_id:
                    lead.monday_item_id = monday_item_id
                    db.session.commit()
                    print(f"Lead synced to Monday: {monday_item_id}")
            except Exception as e:
                print(f"Monday.com sync error: {e}")
        
        except Exception as e:
            print(f"Lead creation error: {e}")
            db.session.rollback()
    
    return jsonify({
        'recommendation': recommendation,
        'lead_id': lead_id,
        'answers_count': len(answers)
    }), 200
