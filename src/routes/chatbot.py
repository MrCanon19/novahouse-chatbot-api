from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
import google.generativeai as genai
import os

from src.models.chatbot import db, ChatConversation, ChatMessage, RodoConsent, Lead, AuditLog
from src.knowledge.novahouse_info import PACKAGES, FAQ, COMPANY_INFO, get_package_description, get_all_packages_summary

chatbot_bp = Blueprint('chatbot', __name__)


def _check_admin_key():
    """Return None if ok, or (response, status) tuple if unauthorized."""
    from flask import request
    admin_key = os.getenv('ADMIN_API_KEY')
    if not admin_key:
        return None
    header = request.headers.get('X-ADMIN-API-KEY') or request.headers.get('X-API-KEY')
    if header == admin_key:
        return None
    return (jsonify({'error': 'Unauthorized'}), 401)

# Konfiguracja Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

SYSTEM_PROMPT = f"""Jesteś pomocnym asystentem NovaHouse — eksperta od wykończenia wnętrz.

{COMPANY_INFO}

PAKIETY WYKOŃCZENIOWE:
{get_all_packages_summary()}

📋 TW OJE ZADANIA:
1. Powitaj ciepło i profesjonalnie każdego gościa
2. Zadawaj pytania by zrozumieć potrzeby klienta (metraż, budżet, styl)
3. Rekomenduj odpowiedni pakiet na podstawie odpowiedzi
4. Odpowiadaj krótko, precyzyjnie i profesjonalnie (ale "na luzie" - nie formalno)
5. Zachęcaj do konsultacji i pozostawienia kontaktu

🎯 STYL KOMUNIKACJI:
- Krótkie, klarowne zdania (maksymalnie 2-3 zdania na raz)
- Naturalne, nie sztywne sformułowania
- Empaticzny ton - słuchamy, rozumiemy, pomagamy
- Na "ty" - bądź przyjazny ale profesjonalny
- Jeśli pytanie jest skomplikowane - zaproponuj rozmowę z ekspertem

💡 WAŻNE ZASADY:
- Zawsze odpowiadaj PO POLSKU
- Nie wymyślaj faktów - jeśli nie wiesz - powiedz że sprawdzisz
- Nie gwarantuj cen - mów "orientacyjnie" lub "od... do..."
- Zawsze miej gotową rekomendację kontaktu: +48 585 004 663
- Jeśli ktoś wykaże zainteresowanie - zawsze zaproponuj pozostawienie maila/telefonu

🚫 CZEGO NIE ROBIĆ:
- Nie bądź zbyt formalny lub rzeczowy
- Nie udzielaj porad poza tematem wykończenia
- Nie obiecuj niemożliwych terminów bez konsultacji z szefem

ROZPOCZĘCIE KONWERSACJI:
Zawsze zaczynaj od powitania i pytania co klienta interesuje. Bądź ciepły!
"""

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        session_id = data.get('session_id', 'default')
        
        # Znajdź lub utwórz konwersację
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            conversation = ChatConversation(
                session_id=session_id,
                started_at=datetime.now(timezone.utc)
            )
            db.session.add(conversation)
            db.session.commit()
        
        # Zapisz wiadomość użytkownika
        user_msg = ChatMessage(
            conversation_id=conversation.id,
            message=user_message,
            sender='user',
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(user_msg)
        
        # Sprawdź czy wiadomość dotyczy FAQ
        bot_response = check_faq(user_message)
        
        # Jeśli nie znaleziono w FAQ, użyj Gemini
        if not bot_response and model:
            try:
                # Pobierz historię konwersacji
                history = ChatMessage.query.filter_by(
                    conversation_id=conversation.id
                ).order_by(ChatMessage.timestamp.desc()).limit(10).all()
                
                context = SYSTEM_PROMPT + "\n\nHistoria rozmowy:\n"
                for msg in reversed(history):
                    context += f"{msg.sender}: {msg.message}\n"
                
                context += f"\nuser: {user_message}\n\nOdpowiedz jako asystent NovaHouse:"
                
                response = model.generate_content(context)
                bot_response = response.text
                
            except Exception as e:
                print(f"Gemini API error: {e}")
                bot_response = "Przepraszam, mam problem z odpowiedzią. Czy mogę pomóc w czymś konkretnym dotyczącym naszych pakietów wykończeniowych?"
        
        # Fallback jeśli nie ma Gemini i nie ma FAQ
        if not bot_response:
            bot_response = get_default_response(user_message)
        
        # Zapisz odpowiedź bota
        bot_msg = ChatMessage(
            conversation_id=conversation.id,
            message=bot_response,
            sender='bot',
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(bot_msg)
        db.session.commit()
        
        return jsonify({
            'response': bot_response,
            'session_id': session_id,
            'conversation_id': conversation.id
        }), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

def check_faq(message):
    """Sprawdź czy wiadomość dotyczy FAQ"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['jak długo', 'ile trwa', 'czas', 'termin', 'ile czasu']):
        return FAQ['jak_dlugo_trwa']
    
    if any(word in message_lower for word in ['materiały', 'cena obejmuje', 'co zawiera', 'co dostanę']):
        return FAQ['czy_wlaczone_materialy']
    
    if any(word in message_lower for word in ['dostosować', 'zmienić', 'modyfikacja', 'elastyczny', 'zmiana']):
        return FAQ['mozna_dostosowac']
    
    if 'gwarancja' in message_lower:
        return FAQ['gwarancja']
    
    if any(word in message_lower for word in ['płatność', 'zapłata', 'koszt', 'ile kosztuje', 'cena', 'wycena']):
        return FAQ.get('ile_kosztuje', FAQ['platnosc'])
    
    if any(word in message_lower for word in ['produkt', 'materiały', 'wyposażenie', 'urządzenia']):
        return FAQ.get('produkty', 'Mamy szeroką gamę produktów od standardowych do luksusowych marek.')
    
    if any(word in message_lower for word in ['etap', 'proces', 'przebieg', 'jak działacie']):
        return FAQ.get('etapy', 'Nasz proces to: konsultacja → projekt → wycena → umowa → realizacja → odbiór.')
    
    if 'projekt' in message_lower and any(word in message_lower for word in ['potrzebny', 'czy', 'konieczny']):
        return FAQ.get('czy_potrzebny_projekt', 'Projekt jest bardzo pomocny w pełnym zaplanowaniu budżetu.')
    
    if any(word in message_lower for word in ['smart', 'automatyka', 'inteligentny dom', 'automatyzacja']):
        return FAQ.get('smart_home', 'Smart home jest dostępne w pakietach Premium i Luxury.')
    
    # Sprawdź pytania o konkretne pakiety
    if 'premium' in message_lower:
        return get_package_description('premium')
    if 'standard' in message_lower:
        return get_package_description('standard')
    if 'luxury' in message_lower or 'luksus' in message_lower:
        return get_package_description('luxury')
    
    # Pytania ogólne o pakiety
    if any(word in message_lower for word in ['pakiety', 'oferta', 'jakie macie', 'co oferujesz', 'co mają']):
        return get_all_packages_summary() + "\n\nO który pakiet chciałbyś dowiedzieć się więcej?"
    
    # Powitania
    greetings = ['cześć', 'dzień dobry', 'witam', 'hej', 'hello', 'siema', 'elo', 'co tam']
    if any(greeting in message_lower for greeting in greetings):
        return "Cześć! 👋 Jestem asystentem NovaHouse. Pomagam w wyborze idealnego pakietu wykończeniowego. Jakie są Twoje potrzeby — remontujemy mieszkanie czy dom?"
    
    return None


def get_default_response(message: str) -> str:
    """Fallback response when no FAQ or model answer is available."""
    return (
        "Dziękuję za pytanie! 😊\n\n"
        "Oferujemy kompleksowe wykończenie mieszkań w trzech pakietach: Standard, Premium i Luxury.\n\n"
        "Chętnie odpowiem na Twoje pytania — możesz zapytać o:\n"
        "• Cenę i budżet\n"
        "• Dostępne materiały\n"
        "• Czas realizacji\n"
        "• Gwarancję i warunki\n\n"
        "Lub jeśli wolisz — skontaktuj się z nami: +48 585 004 663"
    )

@chatbot_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """Get conversation history"""
    try:
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        
        if not conversation:
            return jsonify({'messages': []}), 200
        
        messages = ChatMessage.query.filter_by(
            conversation_id=conversation.id
        ).order_by(ChatMessage.timestamp.asc()).all()
        
        return jsonify({
            'messages': [{
                'message': msg.message,
                'sender': msg.sender,
                'timestamp': msg.timestamp.isoformat()
            } for msg in messages]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/rodo-consent', methods=['POST'])
def save_rodo_consent():
    """Zapisz zgodę RODO użytkownika"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        # Sprawdź czy zgoda już istnieje
        existing_consent = RodoConsent.query.filter_by(session_id=session_id).first()
        
        if existing_consent:
            return jsonify({
                'success': True,
                'message': 'Zgoda RODO już zapisana'
            }), 200
        
        # Zapisz nową zgodę
        consent = RodoConsent(
            session_id=session_id,
            consent_given=data.get('consent_given', True),
            consent_date=datetime.now(timezone.utc),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500]
        )
        
        db.session.add(consent)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Zgoda RODO zapisana pomyślnie'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error saving RODO consent: {e}")
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/delete-my-data', methods=['DELETE'])
def delete_user_data():
    """Usuń dane użytkownika (prawo do bycia zapomnianym - RODO Art. 17)"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        # Usuń konwersację i wszystkie powiązane wiadomości (cascade)
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if conversation:
            db.session.delete(conversation)
        
        # Usuń leady powiązane z sesją
        Lead.query.filter_by(session_id=session_id).delete()
        
        # Usuń zgodę RODO
        RodoConsent.query.filter_by(session_id=session_id).delete()
        
        db.session.commit()

        # Audit the deletion
        try:
            audit = AuditLog(
                action='delete',
                session_id=session_id,
                ip_address=request.remote_addr,
                details=f"Deleted conversation and related leads/consent for session {session_id}"
            )
            db.session.add(audit)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return jsonify({
            'success': True,
            'message': 'Wszystkie Twoje dane zostały usunięte zgodnie z RODO'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user data: {e}")
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/rodo-consent/<session_id>', methods=['GET'])
def get_rodo_consent(session_id):
    """Pobierz zapis zgody RODO dla danej sesji"""
    try:
        consent = RodoConsent.query.filter_by(session_id=session_id).first()
        if not consent:
            return jsonify({'error': 'Consent not found'}), 404
        return jsonify(consent.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/consents', methods=['GET'])
def list_consents():
    """Admin endpoint: list consents with simple pagination (admin key required)"""
    unauthorized = _check_admin_key()
    if unauthorized:
        return unauthorized

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        query = RodoConsent.query.order_by(RodoConsent.consent_date.desc())
        total = query.count()
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        return jsonify({
            'page': page,
            'per_page': per_page,
            'total': total,
            'consents': [c.to_dict() for c in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/audit', methods=['GET'])
def list_audit():
    """Admin endpoint: list audit logs with pagination and optional filters"""
    unauthorized = _check_admin_key()
    if unauthorized:
        return unauthorized

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        action = request.args.get('action')
        session_id = request.args.get('session_id')

        query = AuditLog.query
        if action:
            query = query.filter(AuditLog.action == action)
        if session_id:
            query = query.filter(AuditLog.session_id == session_id)

        total = query.count()
        items = query.order_by(AuditLog.timestamp.desc()).limit(per_page).offset((page - 1) * per_page).all()

        return jsonify({
            'page': page,
            'per_page': per_page,
            'total': total,
            'items': [a.to_dict() for a in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/audit/cleanup', methods=['POST'])
def cleanup_audit_endpoint():
    """Admin endpoint to cleanup audit logs older than N days (default 90)."""
    unauthorized = _check_admin_key()
    if unauthorized:
        return unauthorized

    try:
        data = request.get_json() or {}
        days = int(data.get('days', 90))
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        deleted = AuditLog.query.filter(AuditLog.timestamp < cutoff).delete()
        db.session.commit()

        # record audit of cleanup
        try:
            audit = AuditLog(action='cleanup', session_id=None, ip_address=request.remote_addr, details=f'Purged {deleted} audit logs older than {days} days')
            db.session.add(audit)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return jsonify({'deleted': deleted}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/export-data/<session_id>', methods=['GET'])
def export_user_data(session_id):
    """Eksportuj wszystkie dane powiązane z sesją (konwersacje, wiadomości, leady, zgoda)"""
    # optional admin key check
    unauthorized = _check_admin_key()
    if unauthorized:
        return unauthorized

    try:
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        messages = []
        if conversation:
            msgs = ChatMessage.query.filter_by(conversation_id=conversation.id).order_by(ChatMessage.timestamp.asc()).all()
            messages = [
                {'id': m.id, 'message': m.message, 'sender': m.sender, 'timestamp': m.timestamp.isoformat()}
                for m in msgs
            ]

        leads = [l.to_dict() for l in Lead.query.filter_by(session_id=session_id).all()]
        consent = RodoConsent.query.filter_by(session_id=session_id).first()

        result = {
            'session_id': session_id,
            'conversation_id': conversation.id if conversation else None,
            'messages': messages,
            'leads': leads,
            'consent': consent.to_dict() if consent else None
        }

        # Audit the export
        try:
            audit = AuditLog(
                action='export',
                session_id=session_id,
                ip_address=request.remote_addr,
                details=f"Exported data for session {session_id}"
            )
            db.session.add(audit)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
