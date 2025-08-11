from flask import Blueprint, request, jsonify
from src.models.chatbot import db, Conversation, Lead, Intent, Entity
import json
import uuid
import re
import random
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

class NovaHouseChatbot:
    """Główna klasa chatbota NovaHouse"""
    
    def __init__(self):
        self.intents = {}
        self.entities = {}
    
    def load_intents_and_entities(self):
        """Ładowanie intencji i encji z bazy danych"""
        from flask import current_app
        
        with current_app.app_context():
            self.intents = {}
            self.entities = {}
            
            # Ładowanie intencji
            intents = Intent.query.all()
            for intent in intents:
                self.intents[intent.name] = {
                    'training_phrases': json.loads(intent.training_phrases),
                    'response_templates': json.loads(intent.response_templates)
                }
            
            # Ładowanie encji
            entities = Entity.query.all()
            for entity in entities:
                self.entities[entity.name] = json.loads(entity.values)
    
    def extract_entities(self, text):
        """Wyciąganie encji z tekstu"""
        extracted = {}
        text_lower = text.lower()
        
        for entity_name, values in self.entities.items():
            for value in values:
                if value.lower() in text_lower:
                    extracted[entity_name] = value
                    break
        
        return extracted
    
    def classify_intent(self, text):
        """Klasyfikacja intencji na podstawie tekstu"""
        text_lower = text.lower()
        best_match = None
        best_score = 0
        
        for intent_name, intent_data in self.intents.items():
            score = 0
            for phrase in intent_data['training_phrases']:
                # Proste dopasowanie słów kluczowych
                phrase_words = phrase.lower().split()
                text_words = text_lower.split()
                
                matches = sum(1 for word in phrase_words if word in text_words)
                if matches > 0:
                    score += matches / len(phrase_words)
            
            if score > best_score:
                best_score = score
                best_match = intent_name
        
        return best_match if best_score > 0.3 else 'default'
    
    def generate_response(self, intent, entities, context=None):
        """Generowanie odpowiedzi na podstawie intencji i encji"""
        
        if intent == 'zapytanie_o_pakiety':
            return self._handle_package_inquiry(entities)
        elif intent == 'pytanie_o_ceny':
            return self._handle_price_inquiry(entities)
        elif intent == 'umowienie_konsultacji' or intent == 'umowienie_spotkania':
            return self._handle_meeting_request(entities)
        elif intent == 'pytanie_o_kontakt' or intent == 'kontakt_z_doradca':
            return self._handle_contact_inquiry()
        elif intent == 'powitanie':
            return self._handle_greeting()
        elif intent == 'pozegnanie':
            return self._handle_goodbye()
        elif intent == 'pytanie_o_materialy':
            return self._handle_materials_inquiry()
        elif intent == 'pytanie_o_czas_realizacji':
            return self._handle_time_inquiry()
        else:
            return self._handle_default()
    
    def _handle_package_inquiry(self, entities):
        """Obsługa pytań o pakiety wykończeniowe"""
        if 'pakiet_wykonczeniowy' in entities:
            package = entities['pakiet_wykonczeniowy']
            return f"Pakiet {package.title()} to doskonały wybór! Zawiera wysokiej jakości materiały i profesjonalne wykonanie. Czy chciałbyś poznać szczegóły tego pakietu lub porównać go z innymi opcjami?"
        else:
            return """Oferujemy 4 główne pakiety wykończeniowe:

🟡 **Pakiet Waniliowy** - podstawowy standard z solidnymi materiałami
🟠 **Pakiet Pomarańczowy** - podwyższony standard z lepszymi wykończeniami  
🟤 **Pakiet Cynamonowy** - wysoki standard z markowymi materiałami
🟫 **Pakiet Szafranowy** - najwyższy standard premium

Każdy pakiet można dostosować do Twoich potrzeb. O którym pakiecie chciałbyś dowiedzieć się więcej?"""
    
    def _handle_price_inquiry(self, entities):
        """Obsługa pytań o ceny"""
        package = entities.get('pakiet_wykonczeniowy', '')
        size = entities.get('metraz_lokalu', '')
        
        response = "Ceny naszych pakietów zależą od metrażu i wybranego standardu wykończenia. "
        
        if package:
            response += f"Dla pakietu {package.title()} "
        if size:
            response += f"o powierzchni {size} "
            
        response += "przygotujemy dla Ciebie indywidualną wycenę. Czy chciałbyś umówić się na bezpłatną konsultację, podczas której przedstawimy szczegółową ofertę?"
        
        return response
    
    def _handle_meeting_request(self, entities):
        """Obsługa próśb o umówienie spotkania"""
        return """Świetnie! Chętnie umówimy spotkanie, aby omówić Twoje potrzeby.

Możesz wybrać:
📞 **Konsultację telefoniczną** - szybko i wygodnie
🏢 **Spotkanie w naszym biurze** - pełna prezentacja materiałów
🏠 **Wizytę w Twoim mieszkaniu** - dokładny pomiar i wycena

Podaj proszę swój numer telefonu, a nasz konsultant skontaktuje się z Tobą w ciągu 24 godzin."""
    
    def _handle_contact_inquiry(self):
        """Obsługa pytań o kontakt"""
        return """📞 **Kontakt z NovaHouse:**

🏢 **Biuro:** ul. Przykładowa 123, Gdańsk
📱 **Telefon:** +48 123 456 789
📧 **Email:** kontakt@novahouse.pl
🌐 **Strona:** www.novahouse.pl

**Godziny pracy:**
Pon-Pt: 8:00-18:00
Sob: 9:00-15:00

Czy chciałbyś umówić się na spotkanie?"""
    
    def _handle_greeting(self):
        """Obsługa powitań"""
        return """Cześć! 👋 Witaj w NovaHouse!

Jestem Twoim asystentem i pomogę Ci w:
🏠 Wyborze pakietu wykończeniowego
💰 Uzyskaniu informacji o cenach  
📅 Umówieniu spotkania z konsultantem
📋 Odpowiedzi na pytania o nasze usługi

Jak mogę Ci pomóc?"""
    
    def _handle_goodbye(self):
        """Obsługa pożegnań"""
        return "Dziękuję za rozmowę! Jeśli będziesz mieć jakieś pytania, śmiało pisz. Miłego dnia! 😊"
    
    def _handle_materials_inquiry(self):
        """Obsługa pytań o materiały"""
        return """Używamy tylko wysokiej jakości materiałów od sprawdzonych dostawców:

🔨 **Materiały budowlane:** Renomowane marki europejskie
🎨 **Farby i lakiery:** Dulux, Tikkurila, Benjamin Moore
🚿 **Armatura łazienkowa:** Grohe, Hansgrohe, Kohlert
⚡ **Instalacje elektryczne:** Legrand, Schneider Electric
🏠 **Podłogi:** Tarkett, Quick-Step, Barlinek

W każdym pakiecie znajdziesz szczegółową specyfikację materiałów. Chcesz poznać szczegóły dla konkretnego pakietu?"""
    
    def _handle_time_inquiry(self):
        """Obsługa pytań o czas realizacji"""
        return """Czas realizacji zależy od zakresu prac i metrażu:

⏱️ **Mieszkanie do 50m²:** 4-6 tygodni
⏱️ **Mieszkanie 50-80m²:** 6-8 tygodni  
⏱️ **Mieszkanie powyżej 80m²:** 8-12 tygodni

**Etapy realizacji:**
1. Pomiary i projekt (1 tydzień)
2. Prace rozbiórkowe (1-2 dni)
3. Instalacje (1-2 tygodnie)
4. Wykończenia (2-4 tygodnie)
5. Sprzątanie i odbiór (1-2 dni)

Podaj metraż swojego mieszkania, a określimy dokładny harmonogram!"""
    
    def _handle_default(self):
        """Obsługa nierozpoznanych zapytań"""
        return """Przepraszam, nie jestem pewien jak odpowiedzieć na Twoje pytanie. 

Mogę pomóc Ci w:
• Informacjach o pakietach wykończeniowych
• Cenach i wycenach
• Umówieniu spotkania z konsultantem
• Kontakcie z firmą

Możesz też napisać "konsultant", a przekażę Cię do naszego specjalisty."""

# Inicjalizacja chatbota zostanie wykonana w endpoincie
chatbot = None

def get_chatbot():
    """Funkcja do pobrania instancji chatbota z lazy loading"""
    global chatbot
    if chatbot is None:
        chatbot = NovaHouseChatbot()
        chatbot.load_intents_and_entities()
    return chatbot

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Główny endpoint do rozmowy z chatbotem"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not message:
            return jsonify({'error': 'Wiadomość nie może być pusta'}), 400
        
        # Pobranie instancji chatbota
        chatbot = get_chatbot()
        
        # Klasyfikacja intencji i wyciągnięcie encji
        intent = chatbot.classify_intent(message)
        entities = chatbot.extract_entities(message)
        
        # Generowanie odpowiedzi
        response = chatbot.generate_response(intent, entities)
        
        # Zapisanie konwersacji do bazy danych
        conversation = Conversation(
            session_id=session_id,
            user_message=message,
            bot_response=response,
            intent=intent,
            entities=json.dumps(entities)
        )
        db.session.add(conversation)
        db.session.commit()
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'intent': intent,
            'entities': entities
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/lead', methods=['POST'])
def create_lead():
    """Endpoint do tworzenia leadów"""
    try:
        data = request.get_json()
        
        lead = Lead(
            session_id=data.get('session_id'),
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            interested_package=data.get('interested_package'),
            property_size=data.get('property_size'),
            property_type=data.get('property_type'),
            location=data.get('location'),
            additional_info=data.get('additional_info')
        )
        
        db.session.add(lead)
        db.session.commit()
        
        return jsonify({
            'message': 'Lead został utworzony pomyślnie',
            'lead_id': lead.id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Endpoint do pobierania historii konwersacji"""
    try:
        conversations = Conversation.query.filter_by(session_id=session_id).order_by(Conversation.timestamp).all()
        return jsonify([conv.to_dict() for conv in conversations])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/intents', methods=['GET'])
def get_intents():
    """Endpoint do pobierania listy intencji"""
    try:
        intents = Intent.query.all()
        return jsonify([intent.to_dict() for intent in intents])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/entities', methods=['GET'])
def get_entities():
    """Endpoint do pobierania listy encji"""
    try:
        entities = Entity.query.all()
        return jsonify([entity.to_dict() for entity in entities])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

