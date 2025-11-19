import json
import os
import re
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  openai package not installed - GPT disabled")

from src.knowledge.novahouse_info import (
    COMPANY_INFO,
    COMPANY_STATS,
    COVERAGE_AREAS,
    FAQ,
    PRODUCT_PARTNERS,
    TEAM_INFO,
    WHY_CHOOSE_US,
    get_client_reviews_summary,
    get_package_description,
    get_portfolio_list,
    get_process_overview,
)
from src.models.chatbot import AuditLog, ChatConversation, ChatMessage, Lead, RodoConsent, db

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/health", methods=["GET"])
def chatbot_health():
    """Health check endpoint for chatbot service"""
    return jsonify({"status": "healthy", "service": "chatbot"}), 200


def process_chat_message(user_message: str, session_id: str) -> dict:
    """
    Process chat message and return bot response
    Used by both REST API and WebSocket

    Args:
        user_message: User's message text
        session_id: Session identifier

    Returns:
        dict with 'response', 'session_id', 'conversation_id'
    """
    try:
        # Znajdź lub utwórz konwersację
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            conversation = ChatConversation(
                session_id=session_id,
                started_at=datetime.now(timezone.utc),
                context_data=json.dumps({}),
            )
            db.session.add(conversation)
            db.session.commit()

        # Load context
        context_memory = json.loads(conversation.context_data or "{}")

        # Extract and update context from user message
        context_memory = extract_context(user_message, context_memory)
        conversation.context_data = json.dumps(context_memory)

        # Zapisz wiadomość użytkownika
        user_msg = ChatMessage(
            conversation_id=conversation.id,
            message=user_message,
            sender="user",
            timestamp=datetime.now(timezone.utc),
        )
        db.session.add(user_msg)

        # Sprawdź czy wiadomość dotyczy FAQ
        bot_response = check_faq(user_message)

        # Jeśli nie znaleziono w FAQ, użyj AI (OpenAI GPT)
        if not bot_response and openai_client:
            try:
                # Pobierz historię konwersacji
                history = (
                    ChatMessage.query.filter_by(conversation_id=conversation.id)
                    .order_by(ChatMessage.timestamp.desc())
                    .limit(10)
                    .all()
                )

                context = "\n".join(
                    [
                        f"{'User' if msg.sender == 'user' else 'Bot'}: {msg.message}"
                        for msg in reversed(history[:-1])  # Exclude current message
                    ]
                )

                # Add memory context
                memory_prompt = ""
                if context_memory:
                    memory_items = []
                    if context_memory.get("name"):
                        memory_items.append(f"Imię: {context_memory['name']}")
                    if context_memory.get("city"):
                        memory_items.append(f"Miasto: {context_memory['city']}")
                    if context_memory.get("square_meters"):
                        memory_items.append(f"Metraż: {context_memory['square_meters']}m²")
                    if context_memory.get("package"):
                        memory_items.append(f"Interesujący pakiet: {context_memory['package']}")
                    if memory_items:
                        memory_prompt = "\n\nZapamiętane info o kliencie:\n" + "\n".join(
                            memory_items
                        )

                print(f"[OpenAI GPT] Przetwarzanie: {user_message[:50]}...")
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT + memory_prompt},
                    {"role": "user", "content": f"Context:\n{context}\n\nUser: {user_message}"},
                ]
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",  # Wracam do 4o-mini - szybszy, stabilniejszy
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7,
                )
                bot_response = response.choices[0].message.content
                print(f"[OpenAI GPT-5 nano] Raw response: {repr(bot_response)}")
                print(
                    f"[OpenAI GPT-5 nano] Odpowiedź: {bot_response[:100] if bot_response else 'PUSTA'}..."
                )

            except (ValueError, AttributeError, ConnectionError) as e:
                print(f"[GPT ERROR] {type(e).__name__}: {e}")
                bot_response = "Przepraszam, wystąpił problem z przetwarzaniem Twojej wiadomości. Czy możesz spytać inaczej?"
            except Exception as e:
                print(f"[GPT UNEXPECTED ERROR] {type(e).__name__}: {e}")
                bot_response = "Przepraszam, wystąpił problem z przetwarzaniem Twojej wiadomości. Czy możesz spytać inaczej?"
        elif not bot_response:
            print("[WARNING] Brak OpenAI API key - ustaw OPENAI_API_KEY")

        # Fallback jeśli nadal brak odpowiedzi
        if not bot_response:
            print("[FALLBACK] Używam domyślnej odpowiedzi")
            bot_response = "Dziękuję za wiadomość! Jak mogę Ci pomóc? Możesz zapytać o nasze pakiety, ceny, realizacje czy proces wykończenia."

        # Zapisz odpowiedź bota
        bot_msg = ChatMessage(
            conversation_id=conversation.id,
            message=bot_response,
            sender="bot",
            timestamp=datetime.now(timezone.utc),
        )
        db.session.add(bot_msg)
        db.session.commit()

        return {
            "response": bot_response,
            "session_id": session_id,
            "conversation_id": conversation.id,
        }

    except SQLAlchemyError as e:
        print(f"Database error in chat processing: {e}")
        db.session.rollback()
        return {
            "response": "Przepraszam, problem z bazą danych. Spróbuj ponownie.",
            "session_id": session_id,
            "conversation_id": None,
        }
    except Exception as e:
        print(f"Unexpected chat processing error: {e}")
        db.session.rollback()
        return {
            "response": "Przepraszam, wystąpił błąd. Spróbuj ponownie.",
            "session_id": session_id,
            "conversation_id": None,
            "error": str(e),
        }


def _check_admin_key():
    """Return None if ok, or (response, status) tuple if unauthorized."""
    from flask import request

    admin_key = os.getenv("ADMIN_API_KEY")
    if not admin_key:
        return None
    header = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
    if header == admin_key:
        return None
    return (jsonify({"error": "Unauthorized"}), 401)


# Konfiguracja AI (tylko OpenAI GPT)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if OPENAI_API_KEY and OPENAI_AVAILABLE:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    AI_PROVIDER = "openai"
    print("✅ OpenAI GPT-4o-mini enabled (proven & reliable)")
else:
    openai_client = None
    AI_PROVIDER = None
    print("⚠️  No AI configured - set OPENAI_API_KEY")

SYSTEM_PROMPT = f"""Jesteś pomocnym asystentem NovaHouse — eksperta od wykończenia wnętrz.

{COMPANY_INFO}

📊 NASZE LICZBY:
• {COMPANY_STATS['completed_projects']} zrealizowanych projektów
• {COMPANY_STATS['satisfied_clients']} zadowolonych klientów
• {COMPANY_STATS['projects_before_deadline']} projektów oddanych przed terminem
• {COMPANY_STATS['warranty_years']} lata gwarancji
• Realizacja od {COMPANY_STATS['min_project_duration']}

📍 OBSZARY DZIAŁANIA:
{', '.join(COVERAGE_AREAS['primary'])}

PAKIETY WYKOŃCZENIOWE (mamy 5 pakietów):
1. **Express** (999 zł/m²) - najtańszy, podstawowy, szybki (6-8 tyg)
2. **Express Plus** (1199 zł/m²) - więcej opcji, Standard (6-8 tyg)
3. **Comfort/Szafran** (1499 zł/m²) - premium materiały (8-12 tyg)
4. **Premium** (1999 zł/m²) - najwyższy standard, luksus (10-16 tyg)
5. **Projekt Indywidualny** (1700-5000 zł/m²) - pełna personalizacja

WAŻNE: Gdy klient pyta o konkretne pakiety (np. "najtańsze"), NIE wyświetlaj wszystkich szczegółów wszystkich pakietów!
Pokaż TYLKO te o które pyta, krótko i zwięźle.

🤝 PARTNERZY PRODUKTOWI:
Współpracujemy z najlepszymi: {', '.join(PRODUCT_PARTNERS[:8])} i innymi.

📋 TWOJE ZADANIA:
1. Powitaj ciepło i profesjonalnie każdego gościa
2. Zadawaj pytania by zrozumieć potrzeby klienta (metraż, budżet, styl, lokalizacja)
3. Rekomenduj odpowiedni pakiet na podstawie odpowiedzi
4. Pokaż proces realizacji jeśli klient pyta "jak to działa"
5. Pokaż portfolio gdy klient pyta o realizacje
6. Zachęcaj do konsultacji i pozostawienia kontaktu

🎯 STYL KOMUNIKACJI:
- Krótkie, klarowne zdania (maksymalnie 2-3 zdania na raz)
- Naturalne, nie sztywne sformułowania
- Empatyczny ton - słuchamy, rozumiemy, pomagamy
- Na "ty" - bądź przyjazny ale profesjonalny
- Podkreślaj nasze USP: 94% przed terminem, 36 miesięcy gwarancji, sprawdzone ekipy
- Jeśli pytanie jest skomplikowane - zaproponuj rozmowę z ekspertem

💡 WAŻNE ZASADY:
- Zawsze odpowiadaj PO POLSKU
- Nie wymyślaj faktów - jeśli nie wiesz - powiedz że sprawdzisz
- Nie gwarantuj cen - mów "orientacyjnie" lub "od 949 do 1990 zł/m²"
- Zawsze miej gotową rekomendację kontaktu: +48 585 004 663

🎯 PRECYZYJNA ODPOWIEDŹ NA PYTANIA:
- Gdy klient pyta o "najtańsze pakiety" → odpowiedz KRÓTKO: "Express (999 zł/m²) i Express Plus (1199 zł/m²)"
- Gdy pyta o "najdroższe" → odpowiedz KRÓTKO: "Premium (1999 zł/m²)"
- Gdy pyta o "pakiet Express" → opisz TYLKO ten 1 pakiet w 2-3 zdaniach
- Gdy pyta o "różnice między X a Y" → porównaj TYLKO te 2 pakiety
- Gdy pyta "który dla mnie" → zadaj pytania o budżet i potrzeby, POTEM rekomenduj max 2 pakiety
- NIGDY nie wypisuj szczegółów wszystkich 5 pakietów chyba że klient prosi "pokaż wszystkie"

PRZYKŁADY DOBRYCH ODPOWIEDZI:
✅ "Jakie najtańsze pakiety?"
→ "Najtańsze to Express (999 zł/m²) i Express Plus (1199 zł/m²). Który Cię interesuje?"

✅ "Pokaż pakiet Express"
→ "Express to nasz najbardziej ekonomiczny pakiet za 999 zł/m². Realizacja 6-8 tyg, 150 produktów Basic. Idealny dla wynajmu. Chcesz szczegóły?"

✅ "Jaki pakiet polecacie?"
→ "Zależy od Twojego budżetu i oczekiwań. Co planujesz - mieszkanie do zamieszkania czy pod wynajem?"

❌ ŹLE: Nie wypisuj wszystkich 5 pakietów ze szczegółami jeśli nie pytano o wszystkie!
- Jeśli ktoś wykaże zainteresowanie - zawsze zaproponuj pozostawienie maila/telefonu
- Sprawdź czy klient jest z Trójmiasta, Warszawy lub Wrocławia

🚫 CZEGO NIE ROBIĆ:
- Nie bądź zbyt formalny lub rzeczowy
- Nie udzielaj porad poza tematem wykończenia
- Nie obiecuj niemożliwych terminów bez konsultacji z zespołem

ROZPOCZĘCIE KONWERSACJI:
Zawsze zaczynaj od ciepłego powitania i pytania co klienta interesuje oraz skąd jest (lokalizacja). Bądź ciepły!
"""


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages via REST API"""
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400

        user_message = data["message"]
        session_id = data.get("session_id", "default")

        # Use shared processing function
        result = process_chat_message(user_message, session_id)

        if "error" in result:
            return jsonify({"error": result.get("response")}), 500

        return jsonify(result), 200

    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": "Internal server error"}), 500


def extract_context(message, existing_context):
    """
    Extract context information from user message
    Returns updated context dict with: name, email, city, square_meters, package
    """
    message_lower = message.lower()

    # Extract name (after "jestem", "nazywam się", "mam na imię")
    name_patterns = [
        r"jestem\s+([A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)",
        r"nazywam się\s+([A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)",
        r"mam na imię\s+([A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)",
    ]
    for pattern in name_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            existing_context["name"] = match.group(1)
            break

    # Extract email
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    email_match = re.search(email_pattern, message)
    if email_match:
        existing_context["email"] = email_match.group(0)

    # Extract city
    cities = ["gdańsk", "warszawa", "wrocław", "sopot", "gdynia", "kraków", "poznań", "łódź"]
    for city in cities:
        if city in message_lower:
            existing_context["city"] = city.title()
            break

    # Extract square meters
    sqm_patterns = [r"(\d+)\s*m²", r"(\d+)\s*metrów", r"(\d+)\s*m2", r"(\d+)\s*mkw"]
    for pattern in sqm_patterns:
        match = re.search(pattern, message_lower)
        if match:
            existing_context["square_meters"] = int(match.group(1))
            break

    # Extract interested package
    packages = ["express", "comfort", "premium", "indywidualny"]
    for pkg in packages:
        if pkg in message_lower:
            existing_context["package"] = pkg.title()
            break

    return existing_context


def check_faq(message):
    """Sprawdź czy wiadomość dotyczy FAQ"""
    message_lower = message.lower()

    # Podstawowe FAQ
    if any(
        word in message_lower for word in ["jak długo", "ile trwa", "czas", "termin", "ile czasu"]
    ):
        return FAQ["jak_dlugo_trwa"]

    if any(
        word in message_lower for word in ["materiały", "cena obejmuje", "co zawiera", "co dostanę"]
    ):
        return FAQ["czy_wlaczone_materialy"]

    if any(
        word in message_lower
        for word in ["dostosować", "zmienić", "modyfikacja", "elastyczny", "zmiana"]
    ):
        return FAQ["mozna_dostosowac"]

    if "gwarancja" in message_lower:
        return FAQ["gwarancja"]

    # Najpierw sprawdź pytania o dodatkowe koszty (bardziej specyficzne)
    if any(
        word in message_lower
        for word in ["dodatkowe koszty", "dodatkowe opłaty", "ukryte koszty", "niespodzianki"]
    ):
        return FAQ["dodatkowe_oplaty"]

    # Potem ogólne pytania o koszty
    if any(
        word in message_lower
        for word in ["płatność", "zapłata", "koszt", "ile kosztuje", "cena", "wycena"]
    ):
        return FAQ.get(
            "ile_kosztuje",
            "Ceny zależą od wybranego pakietu i metrażu. Skontaktuj się z nami po szczegóły.",
        )

    if any(word in message_lower for word in ["produkt", "materiały", "wyposażenie", "urządzenia"]):
        return FAQ.get(
            "produkty", "Mamy szeroką gamę produktów od standardowych do luksusowych marek."
        )

    # Nowe FAQ - proces i przebieg
    if any(
        word in message_lower
        for word in ["etap", "proces", "przebieg", "jak działacie", "jak to wygląda", "workflow"]
    ):
        return get_process_overview()

    if "projekt" in message_lower and any(
        word in message_lower for word in ["potrzebny", "czy", "konieczny"]
    ):
        return FAQ.get(
            "czy_potrzebny_projekt", "Projekt jest bardzo pomocny w pełnym zaplanowaniu budżetu."
        )

    if any(
        word in message_lower
        for word in ["smart", "automatyka", "inteligentny dom", "automatyzacja"]
    ):
        return FAQ.get("smart_home", "Smart home jest dostępne w pakietach Premium i Luxury.")

    # Nowe FAQ - terminowość i ekipy
    if any(
        word in message_lower
        for word in ["terminowo", "na czas", "dotrzymanie", "opóźnienie", "spóźnienie"]
    ):
        return FAQ["terminowosc"]

    if any(
        word in message_lower for word in ["ekipa", "ekipy", "fachowcy", "wykonawcy", "pracownicy"]
    ):
        return FAQ["ekipy"]

    # Zakres usług
    if any(
        word in message_lower for word in ["zakres", "co robicie", "czym się zajmujecie", "usługi"]
    ):
        return "Zajmujemy się kompleksowym wykończeniem wnętrz pod klucz: projekt i koncepcja, zakupy i logistyka, koordynacja i nadzór, prace wykończeniowe (remonty, montaż podłóg, drzwi, malowanie), zabudowy stolarskie (kuchnie, szafy, meble na wymiar), sprzątanie i przygotowanie do użytkowania. Oferujemy 4 pakiety (Express, Express Plus, Comfort, Premium) oraz projekty indywidulane. Chcesz poznać szczegóły?"

    # Pytania o konkretny pakiet - przekaż do AI (nie używaj ogólnego FAQ)
    # AI lepiej odpowie precyzyjnie na podstawie system prompt
    # if any(word in message_lower for word in ["co obejmuje", "co wchodzi", "co jest w cenie"]):
    #     return FAQ["co_obejmuje_usluga"]

    # Zabudowy stolarskie
    if any(
        word in message_lower
        for word in ["stolars", "zabudow", "meble", "kuchnia na wymiar", "szafa"]
    ):
        return FAQ["zabudowy_stolarskie"]

    # Lokalizacje
    if any(
        word in message_lower for word in ["gdzie", "lokalizacja", "obszar", "region", "miasto"]
    ):
        return FAQ["gdzie_dzialamy"]

    # Cennik dodatkowy
    if any(
        word in message_lower
        for word in ["cennik", "dodatkow", "extra", "niespodzianki", "ukryte koszty"]
    ):
        return FAQ["cennik_dodatkowy"]

    # Po odbiorze
    if any(
        word in message_lower for word in ["po odbiorze", "po skończeniu", "gotowe", "zakończeni"]
    ):
        return FAQ["po_odbiorze"]

    # Portfolio i realizacje
    if any(
        word in message_lower
        for word in ["realizacj", "portfolio", "przykład", "zdjęcia", "fotki", "referencje"]
    ):
        return get_portfolio_list()

    # Opinie klientów
    if any(
        word in message_lower
        for word in ["opini", "recenzj", "rekomendacj", "co mówią", "feedback"]
    ):
        return get_client_reviews_summary()

    # Partnerzy produktowi
    if any(word in message_lower for word in ["partner", "producent", "marka", "firmy"]):
        partners = ", ".join(PRODUCT_PARTNERS)
        return f"🤝 Współpracujemy z najlepszymi producentami:\n\n{partners}\n\nTo gwarancja jakości materiałów i trwałości wykończenia!"

    # Dlaczego NovaHouse
    if any(
        word in message_lower
        for word in ["dlaczego", "czemu wy", "jakie macie przewagi", "co was wyróżnia"]
    ):
        why = "\n".join([f"✅ {key.title()}: {value}" for key, value in WHY_CHOOSE_US.items()])
        return f"💎 DLACZEGO NOVAHOUSE?\n\n{why}"

    # Zespół
    if any(word in message_lower for word in ["zespół", "team", "pracownicy", "kto", "agnieszka"]):
        return f"👥 NASZ ZESPÓŁ:\n\n{TEAM_INFO['wiceprezes']['name']} - {TEAM_INFO['wiceprezes']['position']}\n\"{TEAM_INFO['wiceprezes']['quote']}\"\n\n{TEAM_INFO['projektanci']['count']}\n{TEAM_INFO['projektanci']['role']}\n\n📌 {TEAM_INFO['projektanci']['note']}"

    # Sprawdź pytania o konkretne pakiety
    if "premium" in message_lower:
        return get_package_description("premium")
    if "standard" in message_lower:
        return get_package_description("standard")
    if "luxury" in message_lower or "luksus" in message_lower:
        return get_package_description("luxury")

    # Pytania ogólne o pakiety - WYŁĄCZONE, niech AI odpowie precyzyjnie
    # Problem: FAQ zwracał wszystkie pakiety nawet gdy pytanie było o "najtańsze pakiety"
    # Teraz AI sam odpowie na podstawie instrukcji w system prompt
    # if any(
    #     word in message_lower
    #     for word in ["pakiety", "oferta", "jakie macie", "co oferujesz", "co mają"]
    # ):
    #     return get_all_packages_summary() + "\n\nO który pakiet chciałbyś dowiedzieć się więcej?"

    # Powitania
    greetings = ["cześć", "dzień dobry", "witam", "hej", "hello", "siema", "elo", "co tam"]
    if any(greeting in message_lower for greeting in greetings):
        return f"Cześć! 👋 Jestem asystentem NovaHouse.\n\n📊 {COMPANY_STATS['completed_projects']} projektów | {COMPANY_STATS['satisfied_clients']} zadowolonych | {COMPANY_STATS['projects_before_deadline']} przed terminem\n\nPomagam w wyborze idealnego pakietu wykończeniowego. Z jakiego jesteś miasta i co planujesz — mieszkanie czy dom?"

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


@chatbot_bp.route("/history/<session_id>", methods=["GET"])
def get_history(session_id):
    """Get conversation history"""
    try:
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()

        if not conversation:
            return jsonify({"messages": []}), 200

        messages = (
            ChatMessage.query.filter_by(conversation_id=conversation.id)
            .order_by(ChatMessage.timestamp.asc())
            .all()
        )

        return (
            jsonify(
                {
                    "messages": [
                        {
                            "message": msg.message,
                            "sender": msg.sender,
                            "timestamp": msg.timestamp.isoformat(),
                        }
                        for msg in messages
                    ]
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/rodo-consent", methods=["POST"])
def save_rodo_consent():
    """Zapisz zgodę RODO użytkownika"""
    try:
        data = request.get_json()
        session_id = data.get("session_id")

        if not session_id:
            return jsonify({"error": "Session ID is required"}), 400

        # Sprawdź czy zgoda już istnieje
        existing_consent = RodoConsent.query.filter_by(session_id=session_id).first()

        if existing_consent:
            return jsonify({"success": True, "message": "Zgoda RODO już zapisana"}), 200

        # Zapisz nową zgodę
        consent = RodoConsent(
            session_id=session_id,
            consent_given=data.get("consent_given", True),
            consent_date=datetime.now(timezone.utc),
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent", "")[:500],
        )

        db.session.add(consent)
        db.session.commit()

        return jsonify({"success": True, "message": "Zgoda RODO zapisana pomyślnie"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error saving RODO consent: {e}")
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/delete-my-data", methods=["DELETE"])
def delete_user_data():
    """Usuń dane użytkownika (prawo do bycia zapomnianym - RODO Art. 17)"""
    try:
        data = request.get_json()
        session_id = data.get("session_id")

        if not session_id:
            return jsonify({"error": "Session ID is required"}), 400

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
                action="delete",
                session_id=session_id,
                ip_address=request.remote_addr,
                details=f"Deleted conversation and related leads/consent for session {session_id}",
            )
            db.session.add(audit)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return (
            jsonify(
                {"success": True, "message": "Wszystkie Twoje dane zostały usunięte zgodnie z RODO"}
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user data: {e}")
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/rodo-consent/<session_id>", methods=["GET"])
def get_rodo_consent(session_id):
    """Pobierz zapis zgody RODO dla danej sesji"""
    try:
        consent = RodoConsent.query.filter_by(session_id=session_id).first()
        if not consent:
            return jsonify({"error": "Consent not found"}), 404
        return jsonify(consent.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/consents", methods=["GET"])
def list_consents():
    """Admin endpoint: list consents with simple pagination (admin key required)"""
    unauthorized = _check_admin_key()
    if unauthorized:
        return unauthorized

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 50))
        query = RodoConsent.query.order_by(RodoConsent.consent_date.desc())
        total = query.count()
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        return (
            jsonify(
                {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "consents": [c.to_dict() for c in items],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/audit", methods=["GET"])
def list_audit():
    """Admin endpoint: list audit logs with pagination and optional filters"""
    unauthorized = _check_admin_key()
    if unauthorized:
        return unauthorized

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 50))
        action = request.args.get("action")
        session_id = request.args.get("session_id")

        query = AuditLog.query
        if action:
            query = query.filter(AuditLog.action == action)
        if session_id:
            query = query.filter(AuditLog.session_id == session_id)

        total = query.count()
        items = (
            query.order_by(AuditLog.timestamp.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
            .all()
        )

        return (
            jsonify(
                {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "items": [a.to_dict() for a in items],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/audit/cleanup", methods=["POST"])
def cleanup_audit_endpoint():
    """Admin endpoint to cleanup audit logs older than N days (default 90)."""
    unauthorized = _check_admin_key()
    if unauthorized:
        return unauthorized

    try:
        data = request.get_json() or {}
        days = int(data.get("days", 90))
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        deleted = AuditLog.query.filter(AuditLog.timestamp < cutoff).delete()
        db.session.commit()

        # record audit of cleanup
        try:
            audit = AuditLog(
                action="cleanup",
                session_id=None,
                ip_address=request.remote_addr,
                details=f"Purged {deleted} audit logs older than {days} days",
            )
            db.session.add(audit)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return jsonify({"deleted": deleted}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/export-data/<session_id>", methods=["GET"])
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
            msgs = (
                ChatMessage.query.filter_by(conversation_id=conversation.id)
                .order_by(ChatMessage.timestamp.asc())
                .all()
            )
            messages = [
                {
                    "id": m.id,
                    "message": m.message,
                    "sender": m.sender,
                    "timestamp": m.timestamp.isoformat(),
                }
                for m in msgs
            ]

        leads = [l.to_dict() for l in Lead.query.filter_by(session_id=session_id).all()]
        consent = RodoConsent.query.filter_by(session_id=session_id).first()

        result = {
            "session_id": session_id,
            "conversation_id": conversation.id if conversation else None,
            "messages": messages,
            "leads": leads,
            "consent": consent.to_dict() if consent else None,
        }

        # Audit the export
        try:
            audit = AuditLog(
                action="export",
                session_id=session_id,
                ip_address=request.remote_addr,
                details=f"Exported data for session {session_id}",
            )
            db.session.add(audit)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/monday-test", methods=["POST"])
def monday_test():
    """Test Monday.com connection and create test item"""
    # Admin key check
    auth_error = _check_admin_key()
    if auth_error:
        return auth_error

    try:
        from src.integrations.monday_client import MondayClient

        monday = MondayClient()

        # Test connection
        if not monday.test_connection():
            return jsonify({"error": "Failed to connect to Monday.com"}), 500

        # Create test item
        test_data = {
            "name": "Test Lead - Novahouse Chatbot",
            "email": "test@novahouse.pl",
            "phone": "123456789",
            "message": "Test integration from chatbot",
            "recommended_package": "premium",
            "confidence_score": 90.0,
            "property_type": "Dom",
            "budget": "150000",
            "interior_style": "Nowoczesny",
        }

        item_id = monday.create_lead_item(test_data)

        if not item_id:
            return jsonify({"error": "Failed to create test item"}), 500

        return (
            jsonify(
                {
                    "message": "Monday.com connection successful",
                    "test_item_id": item_id,
                    "api_key_set": bool(monday.api_key),
                    "board_id_set": bool(monday.board_id),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
