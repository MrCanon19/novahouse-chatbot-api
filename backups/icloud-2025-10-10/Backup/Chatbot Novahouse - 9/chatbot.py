from flask import Blueprint, request, jsonify, current_app
from src.models.user import db
from src.models.chatbot import Conversation, Lead, Intent, Entity
from src.knowledge_base import answer_with_knowledge, get_knowledge_base
from src.analytics import analytics
from src.calendar_integration import get_calendar_integration, format_available_slots_for_chat
from src.email_automation import get_email_automation
import json
import uuid
import re
import random
import time
from datetime import datetime
from src.monday_integration import create_monday_item, get_board_id_by_name, get_board_columns

chatbot_bp = Blueprint("chatbot", __name__)

class NovaHouseChatbot:
    """Glowna klasa chatbota NovaHouse"""
    
    def __init__(self):
        self.intents = {}
        self.entities = {}
    
    def load_intents_and_entities(self):
        """Ładowanie intencji i encji z bazy danych"""
        with current_app.app_context():
            self.intency = {}
            self.entities = {}
            
            # Ładowanie intencji
            intents = Intent.query.all()
            for intent in intents:
                self.intents[intent.name] = {
                    "training_phrases": json.loads(intent.training_phrases),
                    "response_templates": json.loads(intent.response_templates)
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
            for phrase in intent_data["training_phrases"]:
                # Proste dopasowanie słów kluczowych
                phrase_words = phrase.lower().split()
                text_words = text_lower.split()
                
                matches = sum(1 for word in phrase_words if word in text_words)
                if matches > 0:
                    score += matches / len(phrase_words)
            
            if score > best_score:
                best_score = score
                best_match = intent_name
        
        return best_match if best_score > 0.3 else "default"
    
    def generate_response(self, intent, entities):
        """Generowanie odpowiedzi na podstawie intencji i encji"""
        
        if intent == "zapytanie_o_pakiety":
            return self._handle_package_inquiry(entities)
        elif intent == "pytanie_o_ceny":
            return self._handle_price_inquiry(entities)
        elif intent == "umowienie_konsultacji" or intent == "umowienie_spotkania":
            return self._handle_meeting_request(entities)
        elif intent == "pytanie_o_kontakt" or intent == "kontakt_z_doradca":
            return self._handle_contact_inquiry()
        elif intent == "powitanie":
            return self._handle_greeting()
        elif intent == "pozegnanie":
            return self._handle_goodbye()
        elif intent == "pytanie_o_materialy":
            return self._handle_materials_inquiry()
        elif intent == "pytanie_o_czas_realizacji":
            return self._handle_time_inquiry()
        else:
            return self._handle_default()
    
    def _handle_package_inquiry(self, entities):
        """Obsluga pytan o pakiety wykonczeniowe"""
        if "pakiet_wykonczeniowy" in entities:
            package = entities["pakiet_wykonczeniowy"]
            return f"Pakiet {package.title()} to doskonały wybór! Zawiera wysokiej jakości materiały i profesjonalne wykonanie. Czy chciałbyś poznać szczegóły tego pakietu lub porównać go z innymi opcjami?"
        else:
            return """Oferujemy 4 główne pakiety wykończeniowe:\n\n🟡 **Pakiet Waniliowy** - podstawowy standard z solidnymi materiałami\n🟠 **Pakiet Pomarańczowy** - podwyższony standard z lepszymi wykończeniami  \n🟤 **Pakiet Cynamonowy** - wysoki standard z markowymi materiałami\n🟫 **Pakiet Szafranowy** - najwyższy standard premium\n\nKażdy pakiet można dostosować do Twoich potrzeb. O którym pakiecie chciałbyś dowiedzieć się więcej?"""
    
    def _handle_price_inquiry(self, entities):
        """Obsługa pytań o ceny"""
        package = entities.get("pakiet_wykonczeniowy", "")
        size = entities.get("metraz_lokalu", "")
        
        response = "Ceny naszych pakietów zależą od metrażu i wybranego standardu wykończenia. "
        
        if package:
            response += f"Dla pakietu {package.title()} "
        if size:
            response += f"o powierzchni {size} "
            
        response += "przygotujemy dla Ciebie indywidualną wycenę. Czy chciałbyś umów  się na bezpłatną konsultację, podczas której przedstawimy dokładną ofertę?"
        
        return response
    
    def _handle_meeting_request(self, entities):
        """Obsługa próśb o umówienie spotkania"""
        phone_number = entities.get("numer_telefonu")
        email = entities.get("email")
        
        if phone_number:
            # Tworzenie leada w Monday.com
            board_id = get_board_id_by_name("Chat")
            if board_id:
                column_values = {
                    "tekst": f"Nowe zapytanie o spotkanie od {phone_number}",
                    "status": {"label": "Working on it"},
                    "numer_telefonu": phone_number
                }
                
                # Dodanie emaila jeśli dostępny
                if email:
                    column_values["email"] = email
                
                try:
                    new_item = create_monday_item(int(board_id), "topics", "Nowe zapytanie o spotkanie", json.dumps(column_values))
                    
                    if new_item and new_item.get("data") and new_item["data"].get("create_item"):
                        # Sukces Monday.com - wysyłamy email jeśli mamy adres
                        if email:
                            try:
                                email_automation = get_email_automation()
                                client_data = {
                                    'email': email,
                                    'phone': phone_number,
                                    'name': entities.get('imie_klienta', ''),
                                    'interested_package': entities.get('pakiet_wykonczeniowy', ''),
                                    'appointment_booked': False
                                }
                                email_result = email_automation.send_welcome_email(client_data)
                                current_app.logger.info(f"Email automation result: {email_result}")
                            except Exception as e:
                                current_app.logger.error(f"Błąd wysyłania emaila: {e}")
                        
                        return f"Dziękuję! Przekazałem Twoje zapytanie o spotkanie. Nasz konsultant skontaktuje się z Tobą pod numerem {phone_number} w ciągu 24 godzin."
                    else:
                        current_app.logger.error(f"Błąd podczas tworzenia zapytania w monday.com: {new_item}")
                        return "Przepraszam, wystąpił problem podczas tworzenia zapytania w monday.com. Spróbuj ponownie później."
                except Exception as e:
                    current_app.logger.error(f"Wyjątek podczas tworzenia zapytania w monday.com: {e}")
                    return "Przepraszam, wystąpił problem podczas tworzenia zapytania w monday.com. Spróbuj ponownie później."
            else:
                return "Przepraszam, nie mogę znaleźć tablicy \"Chat\" w monday.com. Skontaktuj się z administratorem."
        else:
            return """Świetnie! Chętnie umówimy się na spotkanie, aby omówić Twoje potrzeby.

Możesz wybrać:
📞 **Konsultację telefoniczną** - szybko i wygodnie
🏢 **Spotkanie w naszym biurze** - pełna prezentacja materiałów
🏡 **Wizytę w Twoim domu/mieszkaniu** - szczegółowa wycena i doradztwo

Podaj proszę swój numer telefonu, a my skontaktujemy się z Tobą w ciągu 24 godzin."""
    
    def _handle_contact_inquiry(self):
        """Obsługa pytań o kontakt"""
        return """📞 **Kontakt z NovaHouse:**\n\n🏢 **Biuro:** ul. Przykładowa 123, Gdańsk\n📱 **Telefon:** +48 123 456 789\n📧 **Email:** kontakt@novahouse.pl\n🌐 **Strona:** www.novahouse.pl\n\n**Godziny otwarcia:**\nPon. - Pt.: 9:00 - 17:00\nSobota: 10:00 - 14:00\nNiedziela: Zamknięte\n
Czy mogę jeszcze w czymś pomóc?\n"""
    def _handle_greeting(self):
        """Obsluga powitan"""
        return """Cześć! 👋 Witaj w NovaHouse!\n\nJestem Twoim asystentem i pomogę Ci w:\n🏠 Wyborze pakietu wykończeniowego\n💰 Uzyskaniu informacji o cenach  \n📅 Umówieniu spotkania z doradcą\n✉️ Odpowiedzi na pytania dotyczące naszych usług\n\nJak mogę jeszcze pomóc?\n"""

    def _handle_goodbye(self):
        """Obsluga pozegnan"""
        return "Dziękujemy za rozmowę! Jeśli masz jeszcze jakieś pytania, zapraszamy ponownie. Do zobaczenia! 👋"

    def _handle_materials_inquiry(self):
        """Obsługa pytań o materiały"""
        return """Używamy tylko wysokiej jakości materiałów od sprawdzonych dostawców:\n\n🔨 **Materiały budowlane:** Renomowane marki europejskie\n🎨 **Farby i tynki:** Dulux, Caparol, Beckers\n🚿 **Armatura łazienkowa:** Grohe, Hansgrohe, Roca\n💡 **Oświetlenie:** Philips, Osram, Ledvance\n
W każdym pakiecie znajdziesz szczegółową specyfikację materiałów. Czy chcesz poznać szczegóły dla konkretnego pakietu?"""

    def _handle_time_inquiry(self):
        """Obsługa pytań o czas realizacji"""
        return """Czas realizacji zależy od zakresu prac i metrażu:\n\n⏱️ **Mieszkanie do 50m²:** 4-6 tygodni\n⏱️ **Mieszkanie 50-80m²:** 6-8 tygodni  \n⏱️ **Mieszkanie powyżej 80m²:** 8-12 tygodni\n
**Etapy realizacji:**\n1. Projekt i planowanie (1 tydzień)\n2. Praca przygotowawcza (1-2 dni)\n3. Instalacje (1-2 tygodnie)\n4. Wykończenia (2-4 tygodnie)\n5. Odbiór i sprzątanie (1-2 dni)\n
Podaj metraż swojego mieszkania, a określimy dokładny harmonogram!"""

    def _handle_default(self):
        """Obsługa nierozpoznanych zapytań z wykorzystaniem bazy wiedzy"""
        # Pobierz ostatnią wiadomość użytkownika z kontekstu
        user_message = getattr(self, '_current_message', '')
        
        if user_message:
            try:
                # Użyj bazy wiedzy do wygenerowania odpowiedzi
                knowledge_response = answer_with_knowledge(user_message)
                return knowledge_response
            except Exception as e:
                current_app.logger.error(f"Błąd bazy wiedzy: {e}")
        
        # Fallback do standardowej odpowiedzi
        return """Przepraszamy, nie jestem pewien, jak odpowiedzieć na Twoje pytanie. 

Mogę pomóc Ci w:
• Informacjach o pakietach wykończeniowych
• Cenach i wycenach
• Umówieniu spotkania z doradcą
• Kontakcie z firmą

Możesz też napisz "doradca" lub "kontakt" a przekażemy Cię do odpowiedniej osoby."""


# Inicjalizacja chatbota, only once
chatbot = None


def get_chatbot():
    global chatbot
    if chatbot is None:
        chatbot = NovaHouseChatbot()
        chatbot.load_intents_and_entities()
    return chatbot


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    start_time = time.time()  # Start timing
    lead_created = False
    
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", str(uuid.uuid4()))

        if not message:
            return jsonify({"error": "Wiadomość nie może być pusta"}), 400

        # Pobranie instancji chatbota
        chatbot_instance = get_chatbot()
        
        # Zapisanie aktualnej wiadomości dla bazy wiedzy
        chatbot_instance._current_message = message

        # Klasyfikacja intencji i wyciągnięcie encji z obsługą błędów
        try:
            intent = chatbot_instance.classify_intent(message)
        except Exception as e:
            current_app.logger.error(f"Błąd klasyfikacji intencji: {e}")
            intent = "default"
            
        try:
            entities = chatbot_instance.extract_entities(message)
        except Exception as e:
            current_app.logger.error(f"Błąd wyciągania encji: {e}")
            entities = {}

        # Generowanie odpowiedzi z wykorzystaniem bazy wiedzy
        try:
            response = chatbot_instance.generate_response(intent, entities)
        except Exception as e:
            current_app.logger.error(f"Błąd generowania odpowiedzi: {e}")
            # Fallback response
            response = """Dziękuję za wiadomość! Jestem asystentem NovaHouse i pomogę Ci w:

🏠 **Wyborze pakietu wykończeniowego**
💰 **Uzyskaniu informacji o cenach**  
📅 **Umówieniu spotkania z konsultantem**
📋 **Odpowiedzi na pytania o nasze usługi**

Jak mogę Ci pomóc?"""
        
        # Sprawdzenie czy utworzono lead (dla intencji spotkania)
        if intent in ['umowienie_spotkania', 'umowienie_konsultacji'] and 'numer_telefonu' in entities:
            lead_created = True

        # Zapisanie konwersacji do bazy danych
        try:
            conversation = Conversation(
                session_id=session_id,
                user_message=message,
                bot_response=response,
                intent=intent,
                entities=json.dumps(entities)
            )
            db.session.add(conversation)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Błąd zapisu do bazy: {e}")
        
        # Analytics tracking
        try:
            response_time_ms = int((time.time() - start_time) * 1000)
            analytics.track_conversation(
                session_id=session_id,
                user_message=message,
                bot_response=response,
                intent=intent,
                entities=entities,
                response_time_ms=response_time_ms,
                lead_created=lead_created
            )
        except Exception as e:
            current_app.logger.error(f"Błąd analytics: {e}")

        return jsonify({
            "response": response,
            "session_id": session_id,
            "intent": intent,
            "entities": entities,
            "knowledge_base_enabled": True
        })

    except Exception as e:
        current_app.logger.error(f"Błąd w chatbocie: {e}")
        return jsonify({"error": "Przepraszam, nie mogę połączyć się z serwerem. Spróbuj ponownie."}), 500


@chatbot_bp.route("/lead", methods=["POST"])
def create_lead():
    try:
        data = request.get_json()

        lead = Lead(
            session_id=data.get("session_id"),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            interested_package=data.get("interested_package"),
            property_size=data.get("property_size"),
            property_type=data.nget("property_type"),
            location=data.get("location"),
            additional_info=data.get("additional_info")
        )

        db.session.add(lead)
        db.session.commit()

        return jsonify({
            "message": "Lead został utworzony pomyślnie",
            "lead_id": lead.id
        })

    except Exception as e:
        current_app.logger.error(f"Błąd podczas tworning leada: {e}")
        return jsonify({"error": "Przepraszam, wystąpił błąd podczas tworzenia leada."}), 500


@chatbot_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@chatbot_bp.route("/conversation/<session_id>", methods=["GET"])
def get_conversation(session_id):
    try:
        conversations = Conversation.query.filter_by(session_id=session_id).order_by(Conversation.timestamp).all()
        return jsonify([conv.to_dict() for conv in conversations])

    except Exception as e:
        current_app.logger.error(f"Błąd podczas pobierania konwersacji: {e}")
        return jsonify({"error": "Przepraszam, wystąpił błąd podczas pobierania danych konwersacji."}), 500


@chatbot_bp.route("/intents", methods=["GET"])
def get_intents():
    try:
        intents = Intent.query.all()
        return jsonify([intent.to_dict() for intent in intents])

    except Exception as e:
        current_app.logger.error(f"Błąd podczas pobierania intencji: {e}")
        return jsonify({"error": "Przepraszam, wystąpił błąd podczas pobierania listy intencji."}), 500


@chatbot_bp.route("/entities", methods=["GET"])
def get_entites():
    try:
        entities = Entity.query.all()
        return jsonify([entity.to_dict() for entity in entities])
    except Exception as e:
        current_app.logger.error(f"Błąd podczas pobierania encji: {e}")
        return jsonify({"error": "Przepraszam, wystawił błąd podczas pobierania listy encji."}), 500






@chatbot_bp.route("/intents", methods=["POST"])
def create_intent():
    """Dodaje nową intencję do bazy danych"""
    try:
        data = request.get_json()
        
        # Walidacja danych
        if not data.get("name"):
            return jsonify({"error": "Nazwa intencji jest wymagana"}), 400
        
        if not data.get("training_phrases"):
            return jsonify({"error": "Frazy treningowe są wymagane"}), 400
            
        if not data.get("response_templates"):
            return jsonify({"error": "Szablony odpowiedzi są wymagane"}), 400

        # Sprawdzenie czy intencja już istnieje
        existing_intent = Intent.query.filter_by(name=data["name"]).first()
        if existing_intent:
            return jsonify({"error": f"Intencja '{data['name']}' już istnieje"}), 409

        # Utworzenie nowej intencji
        intent = Intent(
            name=data["name"],
            training_phrases=data["training_phrases"],
            response_templates=data["response_templates"]
        )

        db.session.add(intent)
        db.session.commit()

        return jsonify({
            "message": f"Intencja '{data['name']}' została utworzona pomyślnie",
            "intent_id": intent.id
        }), 201

    except Exception as e:
        current_app.logger.error(f"Błąd podczas tworzenia intencji: {e}")
        return jsonify({"error": "Przepraszam, wystąpił błąd podczas tworzenia intencji."}), 500


@chatbot_bp.route("/entities", methods=["POST"])
def create_entity():
    """Dodaje nową encję do bazy danych"""
    try:
        data = request.get_json()
        
        # Walidacja danych
        if not data.get("name"):
            return jsonify({"error": "Nazwa encji jest wymagana"}), 400
        
        if not data.get("values"):
            return jsonify({"error": "Wartości encji są wymagane"}), 400

        # Sprawdzenie czy encja już istnieje
        existing_entity = Entity.query.filter_by(name=data["name"]).first()
        if existing_entity:
            return jsonify({"error": f"Encja '{data['name']}' już istnieje"}), 409

        # Utworzenie nowej encji
        entity = Entity(
            name=data["name"],
            values=data["values"]
        )

        db.session.add(entity)
        db.session.commit()

        return jsonify({
            "message": f"Encja '{data['name']}' została utworzona pomyślnie",
            "entity_id": entity.id
        }), 201

    except Exception as e:
        current_app.logger.error(f"Błąd podczas tworzenia encji: {e}")
        return jsonify({"error": "Przepraszam, wystąpił błąd podczas tworzenia encji."}), 500


@chatbot_bp.route("/reload", methods=["POST"])
def reload_chatbot():
    """Przeładowuje intencje i encje w chatbocie"""
    try:
        global chatbot
        if chatbot:
            chatbot.load_intents_and_entities()
            return jsonify({"message": "Chatbot został przeładowany pomyślnie"}), 200
        else:
            return jsonify({"error": "Chatbot nie jest zainicjalizowany"}), 500
    except Exception as e:
        current_app.logger.error(f"Błąd podczas przeładowywania chatbota: {e}")
        return jsonify({"error": "Przepraszam, wystąpił błąd podczas przeładowywania chatbota."}), 500

