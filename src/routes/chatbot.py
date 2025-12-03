genai = None  # Dummy dla testów
# Pozwala na patchowanie genai w testach

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
from src.models.chatbot import (
    AuditLog,
    ChatConversation,
    ChatMessage,
    CompetitiveIntel,
    FollowUpTest,
    Lead,
    RodoConsent,
    db,
)

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

        # 1. Check if user wants to book a meeting
        bot_response = check_booking_intent(user_message, context_memory)

        # 2. Check learned FAQs (higher priority - learned from real users)
        if not bot_response:
            bot_response = check_learned_faq(user_message)

        # 3. Then check standard FAQ
        if not bot_response:
            bot_response = check_faq(user_message)

        # 4. Jeśli nie znaleziono w FAQ, ZAWSZE użyj AI (OpenAI GPT) - PRIORYTET!
        if not bot_response:
            if openai_client:
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
                        model="gpt-4o-mini",  # Zoptymalizowany model
                        messages=messages,
                        max_tokens=500,
                        temperature=0.7,
                    )
                    bot_response = response.choices[0].message.content
                    print(
                        f"[OpenAI GPT] Response: {bot_response[:100] if bot_response else 'EMPTY'}..."
                    )

                except Exception as e:
                    print(f"[GPT ERROR] {type(e).__name__}: {e}")
                    # Fallback tylko przy błędzie GPT
                    bot_response = get_default_response(user_message)
            else:
                print("[WARNING] OpenAI nie skonfigurowany - używam fallback")
                bot_response = get_default_response(user_message)

        # Jeśli NADAL brak odpowiedzi (nie powinno się zdarzyć)
        if not bot_response:
            print("[CRITICAL FALLBACK] Używam awaryjnej odpowiedzi")
            bot_response = get_default_response(user_message)

        # Track A/B test response (if user responded to follow-up question)
        if conversation.followup_variant and len(user_message) > 3:
            track_ab_test_response(conversation)

        # Zapisz odpowiedź bota
        bot_msg = ChatMessage(
            conversation_id=conversation.id,
            message=bot_response,
            sender="bot",
            timestamp=datetime.now(timezone.utc),
        )
        db.session.add(bot_msg)

        # Log unknown/unclear questions for FAQ learning
        try:
            from src.models.faq_learning import UnknownQuestion

            # Check if response is generic fallback (potential unknown question)
            is_generic = any(
                phrase in bot_response.lower()
                for phrase in [
                    "jak mogę ci pomóc",
                    "przepraszam",
                    "spróbuj ponownie",
                    "nie jestem pewien",
                    "nie rozumiem",
                ]
            )

            # Log if generic response and not FAQ
            if is_generic and not check_faq(user_message):
                unknown = UnknownQuestion(
                    session_id=session_id,
                    question=user_message,
                    bot_response=bot_response,
                    status="pending",
                )
                db.session.add(unknown)
        except Exception as e:
            print(f"[FAQ Learning] Failed to log: {e}")
            # Don't fail the main flow

        # Check if user is confirming data
        confirmation_intent = check_data_confirmation_intent(user_message)
        existing_lead = Lead.query.filter_by(session_id=session_id).first()

        if confirmation_intent == "confirm" and conversation.awaiting_confirmation:
            # User confirmed - create lead now
            try:
                if not existing_lead:
                    from src.integrations.monday_client import MondayClient

                    # Get message count for lead scoring
                    message_count = ChatMessage.query.filter_by(
                        conversation_id=conversation.id
                    ).count()
                    lead_score = calculate_lead_score(context_memory, message_count)

                    # Generate conversation summary
                    all_messages = (
                        ChatMessage.query.filter_by(conversation_id=conversation.id)
                        .order_by(ChatMessage.timestamp.asc())
                        .all()
                    )
                    conv_summary = generate_conversation_summary(all_messages, context_memory)

                    # Create lead
                    lead = Lead(
                        session_id=session_id,
                        name=context_memory.get("name", "Unknown"),
                        email=context_memory.get("email"),
                        phone=context_memory.get("phone"),
                        location=context_memory.get("city"),
                        property_size=context_memory.get("square_meters"),
                        interested_package=context_memory.get("package"),
                        source="chatbot",
                        status="qualified",  # User confirmed data
                        lead_score=lead_score,
                        conversation_summary=conv_summary,
                        data_confirmed=True,
                        last_interaction=datetime.now(timezone.utc),
                    )

                    db.session.add(lead)
                    db.session.flush()

                    # Generate next action recommendation
                    next_action = suggest_next_best_action(context_memory, lead_score)
                    lead.notes = f"Next Action: {next_action}"

                    # Check for competitive mentions
                    competitor_intel = (
                        CompetitiveIntel.query.filter_by(session_id=session_id)
                        .order_by(CompetitiveIntel.created_at.desc())
                        .first()
                    )
                    competitor_name = competitor_intel.competitor_name if competitor_intel else None

                    # Sync with Monday.com
                    monday = MondayClient(api_key=MONDAY_API_KEY)
                    monday_item_id = monday.create_lead_item(
                        {
                            "name": lead.name,
                            "email": lead.email,
                            "phone": lead.phone,
                            "message": f"Lead Score: {lead_score}/100 | {conv_summary} | Action: {next_action}",
                            "property_type": "Mieszkanie",
                            "budget": context_memory.get("square_meters", ""),
                            "lead_score": lead_score,
                            "competitor_mentioned": competitor_name,
                            "next_action": next_action,
                        }
                    )

                    if monday_item_id:
                        lead.monday_item_id = monday_item_id
                        print(
                            f"[Monday] Confirmed lead created: {monday_item_id} (score: {lead_score})"
                        )
                        # Logowanie zdarzenia API (lead utworzony)
                        try:
                            import sentry_sdk

                            sentry_sdk.capture_message(
                                f"Lead created in Monday.com: {lead.name}, score: {lead_score}"
                            )
                        except ImportError:
                            pass

                    # Alert dla leadów o wysokim priorytecie
                    if lead_score >= 70:
                        try:
                            import sentry_sdk

                            from src.services.email_service import email_service

                            email_service.send_email(
                                to_email=os.getenv("ADMIN_EMAIL", "admin@novahouse.pl"),
                                subject=f"🔥 HIGH PRIORITY LEAD - Score: {lead_score}/100",
                                html_content=f"""
                                <h2>New High-Priority Lead!</h2>
                                <p><strong>Name:</strong> {lead.name}</p>
                                <p><strong>Email:</strong> {lead.email}</p>
                                <p><strong>Score:</strong> {lead_score}</p>
                                <p><strong>Monday.com ID:</strong> {monday_item_id}</p>
                                """,
                            )
                            sentry_sdk.capture_message(
                                f"ALERT: High-priority lead: {lead.name}, score: {lead_score}"
                            )
                        except ImportError:
                            pass

                    # Clear awaiting flag
                    conversation.awaiting_confirmation = False

                    # Add confirmation message to bot response
                    bot_response = (
                        f"✅ Dziękuję za potwierdzenie! Twoje dane zostały zapisane.\n\n"
                        f"Nasz zespół skontaktuje się z Tobą wkrótce.\n\n"
                        f"{bot_response}"
                    )

            except Exception as e:
                print(f"[Confirmed Lead] Error: {e}")

        elif confirmation_intent == "edit":
            # User wants to edit - clear awaiting flag
            conversation.awaiting_confirmation = False
            bot_response = "Oczywiście! Popraw dane które chcesz zmienić, a ja je zaktualizuję. 📝"

        # Check if we should ask for data confirmation
        elif should_ask_for_confirmation(context_memory, conversation):
            conversation.awaiting_confirmation = True
            confirmation_msg = format_data_confirmation_message(context_memory)
            # Append confirmation request to bot response
            bot_response = f"{bot_response}\n\n{confirmation_msg}"

        # Fallback: Auto-create lead if enough data (no confirmation asked)
        elif not conversation.awaiting_confirmation and not existing_lead:
            try:
                has_contact_data = (
                    context_memory.get("name")
                    and context_memory.get("email")
                    or context_memory.get("phone")
                )

                if has_contact_data:
                    from src.integrations.monday_client import MondayClient

                    message_count = ChatMessage.query.filter_by(
                        conversation_id=conversation.id
                    ).count()
                    lead_score = calculate_lead_score(context_memory, message_count)

                    all_messages = (
                        ChatMessage.query.filter_by(conversation_id=conversation.id)
                        .order_by(ChatMessage.timestamp.asc())
                        .all()
                    )
                    conv_summary = generate_conversation_summary(all_messages, context_memory)

                    lead = Lead(
                        session_id=session_id,
                        name=context_memory.get("name", "Unknown"),
                        email=context_memory.get("email"),
                        phone=context_memory.get("phone"),
                        location=context_memory.get("city"),
                        property_size=context_memory.get("square_meters"),
                        interested_package=context_memory.get("package"),
                        source="chatbot",
                        status="new",
                        lead_score=lead_score,
                        conversation_summary=conv_summary,
                        data_confirmed=False,
                        last_interaction=datetime.now(timezone.utc),
                    )

                    db.session.add(lead)
                    db.session.flush()

                    # Check for competitive mentions
                    competitor_intel = (
                        CompetitiveIntel.query.filter_by(session_id=session_id)
                        .order_by(CompetitiveIntel.created_at.desc())
                        .first()
                    )
                    competitor_name = competitor_intel.competitor_name if competitor_intel else None
                    next_action = suggest_next_best_action(context_memory, lead_score)

                    monday = MondayClient(api_key=MONDAY_API_KEY)
                    monday_item_id = monday.create_lead_item(
                        {
                            "name": lead.name,
                            "email": lead.email,
                            "phone": lead.phone,
                            "message": f"Lead Score: {lead_score}/100 | {conv_summary}",
                            "property_type": "Mieszkanie",
                            "budget": context_memory.get("square_meters", ""),
                            "lead_score": lead_score,
                            "competitor_mentioned": competitor_name,
                            "next_action": next_action,
                        }
                    )

                    if monday_item_id:
                        lead.monday_item_id = monday_item_id
                        print(f"[Monday] Auto-lead created: {monday_item_id} (score: {lead_score})")

            except Exception as e:
                print(f"[Auto Lead] Error: {e}")

        db.session.commit()

        # Check for competitive intelligence
        detect_competitive_intelligence(user_message, session_id, context_memory)

        # Generate intelligent follow-up question (with A/B testing)
        follow_up = generate_follow_up_question(
            context_memory, user_message, bot_response, conversation
        )
        if follow_up:
            bot_response = f"{bot_response}\n\n{follow_up}"

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


# Konfiguracja AI (OpenAI GPT + Monday.com)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MONDAY_API_KEY = os.getenv("MONDAY_API_KEY", "")

if OPENAI_API_KEY and OPENAI_AVAILABLE:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    AI_PROVIDER = "openai"
    print("✅ OpenAI GPT-4o-mini enabled (proven & reliable)")
else:
    openai_client = None
    AI_PROVIDER = None
    print("⚠️  No AI configured - set OPENAI_API_KEY")

if MONDAY_API_KEY:
    print("✅ Monday.com API key loaded")
else:
    print("⚠️  No Monday.com API key - set MONDAY_API_KEY")

SYSTEM_PROMPT = f"""Jesteś asystentem NovaHouse — firmy wykańczającej mieszkania pod klucz.

📍 DZIAŁAMY W: {', '.join(COVERAGE_AREAS['primary'])}
📞 KONTAKT: +48 585 004 663

🏆 NASZE WYNIKI:
• {COMPANY_STATS['completed_projects']} ukończonych projektów
• {COMPANY_STATS['satisfied_clients']} zadowolonych klientów
• {COMPANY_STATS['projects_before_deadline']} przed terminem
• {COMPANY_STATS['warranty_years']} lata gwarancji

💰 PAKIETY (ceny/m²):
1. Express - 999 zł (6-8 tyg, Basic)
2. Express Plus - 1199 zł (6-8 tyg, Standard)
3. Comfort - 1499 zł (8-12 tyg, Premium)
4. Premium - 1999 zł (10-16 tyg, Luxury)
5. Indywidualny - 1700-5000 zł (full custom)

📦 CO ZAWIERA KAŻDY PAKIET:
• Projekt + moodboard + konsultacje z projektantem
• Materiały budowlane (farby, kleje, fugi)
• Materiały wykończeniowe (podłogi, drzwi, płytki, armatura)
• Prace: malowanie, montaż podłóg/drzwi, łazienka kompleksowo
• Koordynacja dostaw i ekip
• Sprzątanie końcowe
• 36 miesięcy gwarancji
• 15% rabat na wszystkie materiały

🎯 JAK ODPOWIADAĆ:
1. KONKRETNIE - nie "🤔 Nie jestem pewien" - zawsze podaj informację!
2. ZWIĘŹLE - max 2-3 zdania, potem pytanie
3. CIEPŁO - "na ty", empatycznie, bez sztywności
4. PO POLSKU - zawsze w języku polskim

❗ ZASADY ODPOWIEDZI:
• "ile kosztuje" → podaj cenę konkretnego pakietu (np. "Express 999 zł/m², Express Plus 1199 zł/m²")
• "jak długo" → podaj dokładny czas (np. "Express 6-8 tygodni, Comfort 8-12 tygodni")
• "co zawiera" → wymień konkretne elementy (patrz wyżej)
• "jakie pakiety" → wymień tylko te o które pytano (np. najtańsze = Express i Express Plus)
• "powierzchnia" → zapytaj "Jaki metraż mieszkania?" i zapisz w kontekście
• "lokalizacja" → sprawdź czy jest w: Trójmiasto/Warszawa/Wrocław

🚨 NIGDY NIE UŻYWAJ:
× "🤔 Nie jestem pewien"
× "Przepraszam, nie rozumiem"
× "Spróbuj inaczej zapytać"

✅ ZAMIAST TEGO:
✓ Podaj konkretną odpowiedź z dostępnych informacji
✓ Jeśli brak szczegółu → powiedz "To ustalimy na konsultacji. Dzwonisz czy piszesz?"
✓ Zawsze zakończ pytaniem lub CTA (call to action)

PRZYKŁADY:
❓ "Ile kosztuje wykończenie 50m²?"
✅ "Przy 50m² wyjdzie od ~50 tys (Express) do ~75 tys (Premium). Jaki standard Cię interesuje?"

❓ "Co zawiera pakiet?"
✅ "Komplet: projekt, materiały, prace (malowanie/podłogi/drzwi/łazienka), koordynacja, sprzątanie, 3 lata gwarancji. Pytasz o konkretny pakiet?"

❓ "Jakie macie pakiety?"
✅ "4 pakiety: Express (999 zł/m²), Express Plus (1199), Comfort (1499), Premium (1999). Plus projekty indywidualne. Jaki budżet planujesz?"

🎯 CEL: Pomóc klientowi wybrać pakiet → zebrać: metraż, lokalizację, email/telefon → umówić konsultację

ROZPOCZNIJ OD: Ciepłe powitanie + zapytaj o lokalizację i potrzeby."""


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages via REST API (NEW: with state machine, validation, rate limiting)"""
    try:
        from src.services.message_handler import message_handler

        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400

        user_message = data["message"]
        session_id = data.get("session_id", "default")

        # Rate limiting check (manual - decorator doesn't work here)
        from src.services.rate_limiter import rate_limiter

        allowed, retry_after = rate_limiter.check_rate_limit(
            session_id, "session", max_requests=10, window_seconds=60
        )
        if not allowed:
            return (
                jsonify(
                    {
                        "error": "Rate limit exceeded. Please slow down.",
                        "retry_after": retry_after,
                    }
                ),
                429,
            )

        # NEW: Use refactored message handler with state machine
        result = message_handler.process_message(user_message, session_id)

        if "error" in result and "response" not in result:
            return jsonify({"error": result["error"]}), 500

        return jsonify(result), 200

    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": "Internal server error"}), 500


def calculate_lead_score(context_memory, message_count):
    """
    Calculate lead quality score (0-100)
    Based on: data completeness, engagement, intent signals
    """
    score = 0

    # Data completeness (40 points)
    if context_memory.get("name"):
        score += 10
    if context_memory.get("email"):
        score += 15
    if context_memory.get("phone"):
        score += 15

    # Intent signals (30 points)
    if context_memory.get("package"):
        score += 15
    if context_memory.get("square_meters"):
        score += 10
    if context_memory.get("city"):
        score += 5

    # Engagement (30 points)
    if message_count >= 3:
        score += 10
    if message_count >= 5:
        score += 10
    if message_count >= 8:
        score += 10

    return min(score, 100)


def generate_conversation_summary(messages, context_memory):
    """
    Generate AI summary of conversation for lead notes
    """
    try:
        if not messages or len(messages) < 2:
            return "Krótka konwersacja bez szczegółów."

        # Build summary from context and message count
        summary_parts = []
        if context_memory.get("package"):
            summary_parts.append(f"Zainteresowany: {context_memory.get('package')}")
        if context_memory.get("square_meters"):
            summary_parts.append(f"Metraż: {context_memory.get('square_meters')}m²")
        if context_memory.get("city"):
            summary_parts.append(f"Lokalizacja: {context_memory.get('city')}")

        summary = " | ".join(summary_parts) if summary_parts else "Wstępne pytania ogólne"
        summary += f" | Wiadomości: {len(messages)}"

        return summary

    except Exception as e:
        print(f"[Summary] Error: {e}")
        return "Konwersacja z chatbotem"


def check_data_confirmation_intent(message):
    """
    Check if user is confirming their data
    Returns: 'confirm', 'edit', or None
    """
    message_lower = message.lower().strip()

    confirm_keywords = ["tak", "zgadza", "dobrze", "ok", "poprawnie", "potwierdz"]
    edit_keywords = ["nie", "zmień", "popraw", "błąd", "inaczej", "edytuj"]

    if any(keyword in message_lower for keyword in confirm_keywords):
        return "confirm"
    elif any(keyword in message_lower for keyword in edit_keywords):
        return "edit"

    return None


def should_ask_for_confirmation(context_memory, conversation):
    """
    Determine if we should ask user to confirm their data
    """
    # Check if we have enough data
    has_data = context_memory.get("name") and (
        context_memory.get("email") or context_memory.get("phone")
    )

    # Check if not already confirmed
    not_confirmed = not conversation.awaiting_confirmation

    # Check if lead doesn't exist yet
    no_lead = not Lead.query.filter_by(session_id=conversation.session_id).first()

    return has_data and not_confirmed and no_lead


def format_data_confirmation_message(context_memory):
    """
    Format a nice confirmation message with user's data
    """
    parts = [
        "📋 **Świetnie! Podsumujmy Twoje dane:**\n",
        f"👤 Imię: {context_memory.get('name', 'Nie podano')}",
    ]

    if context_memory.get("email"):
        parts.append(f"📧 Email: {context_memory.get('email')}")
    if context_memory.get("phone"):
        parts.append(f"📱 Telefon: {context_memory.get('phone')}")
    if context_memory.get("city"):
        parts.append(f"📍 Miasto: {context_memory.get('city')}")
    if context_memory.get("square_meters"):
        parts.append(f"📐 Metraż: {context_memory.get('square_meters')}m²")
    if context_memory.get("package"):
        parts.append(f"📦 Pakiet: {context_memory.get('package')}")

    parts.append("\n✅ Czy wszystko się zgadza? (wpisz: TAK lub POPRAW)")

    return "\n".join(parts)


def detect_competitive_intelligence(user_message, session_id, context_memory):
    """
    Detect competitive intelligence signals in conversation
    Returns: intel_type, competitor_name, sentiment, priority
    """
    user_lower = user_message.lower()

    # Competitor mentions
    competitors = [
        "remonteo",
        "remonty",
        "fixly",
        "renovate",
        "home staging",
        "konkurencja",
        "inna firma",
        "inne firmy",
    ]

    competitor_found = None
    for comp in competitors:
        if comp in user_lower:
            competitor_found = comp
            break

    # Price comparison signals
    price_signals = ["tańsze", "droższe", "taniej", "droższ", "porówna", "comparison"]
    is_price_comparison = any(signal in user_lower for signal in price_signals)

    # Feature/quality comparison
    feature_signals = [
        "lepsz",
        "gorsz",
        "jakość",
        "quality",
        "różnica",
        "difference",
        "dlaczego wy",
    ]
    is_feature_comparison = any(signal in user_lower for signal in feature_signals)

    # Loss signal (user went with competitor)
    loss_signals = ["wybrałem", "wybraliśmy", "zdecydował", "zamówił", "umówiłem się z"]
    is_loss = any(signal in user_lower for signal in loss_signals)

    # Sentiment analysis (basic)
    positive_words = ["lepsze", "lepiej", "bardziej", "ciekaw", "interested"]
    negative_words = ["gorsze", "gorzej", "droż", "wolniej", "dłuż"]

    sentiment = "neutral"
    if any(word in user_lower for word in positive_words):
        sentiment = "positive"
    elif any(word in user_lower for word in negative_words):
        sentiment = "negative"

    # Determine intel type and priority
    intel_type = None
    priority = "medium"

    if is_loss:
        intel_type = "loss_to_competitor"
        priority = "high"
    elif competitor_found:
        intel_type = "competitor_mention"
        priority = "high" if is_price_comparison else "medium"
    elif is_price_comparison:
        intel_type = "price_comparison"
        priority = "medium"
    elif is_feature_comparison:
        intel_type = "feature_comparison"
        priority = "medium"

    # Save competitive intel if detected
    if intel_type:
        try:
            intel = CompetitiveIntel(
                session_id=session_id,
                intel_type=intel_type,
                competitor_name=competitor_found if competitor_found else None,
                user_message=user_message,
                context=json.dumps(context_memory),
                sentiment=sentiment,
                priority=priority,
            )
            db.session.add(intel)
            db.session.commit()

            print(f"[Competitive Intel] {intel_type} detected: {competitor_found or 'unknown'}")
            return {
                "detected": True,
                "type": intel_type,
                "competitor": competitor_found,
                "sentiment": sentiment,
                "priority": priority,
            }
        except Exception as e:
            print(f"[Competitive Intel] Error saving: {e}")
            db.session.rollback()

    return {"detected": False}


def track_ab_test_response(conversation):
    """
    Track that user responded to A/B test follow-up question
    """
    try:
        if not conversation.followup_variant:
            return

        # Find the test (we don't know which type, so check all active)
        tests = FollowUpTest.query.filter_by(is_active=True).all()

        for test in tests:
            # Increment response count for the variant shown
            if conversation.followup_variant == "A":
                test.variant_a_responses += 1
            elif conversation.followup_variant == "B":
                test.variant_b_responses += 1

        # Clear variant so we don't double-count
        conversation.followup_variant = None
        db.session.commit()

        print(f"[A/B Test] Response tracked for variant {conversation.followup_variant}")

    except Exception as e:
        print(f"[A/B Test] Error tracking response: {e}")


def get_ab_test_variant(conversation, question_type):
    """
    Get A/B test variant for follow-up question
    Returns: variant ("A" or "B"), question text
    """
    import random

    try:
        # Find active test for this question type
        test = FollowUpTest.query.filter_by(question_type=question_type, is_active=True).first()

        if not test:
            return None, None

        # Random 50/50 split
        variant = random.choice(["A", "B"])

        # Track impression
        if variant == "A":
            test.variant_a_shown += 1
            question = test.variant_a
        else:
            test.variant_b_shown += 1
            question = test.variant_b

        # Save variant to conversation for tracking response
        conversation.followup_variant = variant
        db.session.commit()

        return variant, question

    except Exception as e:
        print(f"[A/B Test] Error: {e}")
        return None, None


def generate_follow_up_question(context_memory, user_message, bot_response, conversation=None):
    """
    Generate intelligent follow-up questions based on conversation context
    Includes A/B testing for optimization
    Increases engagement and gathers more qualifying data
    """
    # Don't add follow-up if already asking for confirmation
    if "Czy wszystko się zgadza?" in bot_response or "TAK lub POPRAW" in bot_response:
        return None

    # Don't add follow-up if it's a booking link
    if "zencal.io" in bot_response or "📅" in bot_response:
        return None

    user_lower = user_message.lower()
    has_package = context_memory.get("package")
    has_sqm = context_memory.get("square_meters")
    has_city = context_memory.get("city")
    has_contact = context_memory.get("email") or context_memory.get("phone")

    # Package interest → ask about square meters (A/B TEST)
    if (
        has_package
        and not has_sqm
        and any(word in user_lower for word in ["pakiet", "express", "comfort", "premium"])
    ):
        if conversation:
            variant, ab_question = get_ab_test_variant(conversation, "package_to_sqm")
            if ab_question:
                return ab_question
        return "💡 **A jaki jest mniej więcej metraż Twojego mieszkania?** To pomoże mi lepiej dopasować ofertę."

    # Square meters given → ask about location (A/B TEST)
    if (
        has_sqm
        and not has_city
        and any(
            word in user_lower
            for word in ["m²", "metr", "mkw", "50", "60", "70", "80", "90", "100"]
        )
    ):
        if conversation:
            variant, ab_question = get_ab_test_variant(conversation, "sqm_to_location")
            if ab_question:
                return ab_question
        return "📍 **W jakim mieście szukasz wykonawcy?** Mamy zespoły w całej Polsce."

    # Price question → ask about budget/financing (A/B TEST)
    if not has_contact and any(
        word in user_lower for word in ["cena", "koszt", "ile", "budget", "cennik"]
    ):
        if conversation:
            variant, ab_question = get_ab_test_variant(conversation, "price_to_budget")
            if ab_question:
                return ab_question
        return "💰 **Masz już określony budżet? Mogę pokazać opcje finansowania i rozłożenia płatności.**"

    # Talked about materials → ask about style preferences
    if any(
        word in user_lower for word in ["materiał", "product", "płytk", "farb", "podłog", "boazeri"]
    ):
        return "🎨 **Jaki styl wnętrz Cię interesuje?** (np. minimalistyczny, industrialny, skandynawski)"

    # Talked about timeline → ask about start date
    if any(word in user_lower for word in ["czas", "długo", "termin", "kiedy", "jak szybko"]):
        return "📅 **Kiedy planujesz rozpocząć projekt?** (np. zaraz, za miesiąc, za 3 miesiące)"

    # General package info → ask if they want personalized quote
    if has_package and has_sqm and not has_contact:
        return "📊 **Chcesz otrzymać szczegółową wycenę dostosowaną do Twojego mieszkania?** Podaj email, wyślę spersonalizowaną ofertę."

    # Nothing specific → gentle engagement
    if not has_contact and len(user_message) < 50:
        return (
            "🤔 **Masz jakieś konkretne pytania? Chętnie opowiem więcej o procesie wykończenia!**"
        )

    return None


def detect_abandonment_risk(conversation, context_memory):
    """
    Detect if user is likely to abandon conversation
    Returns: risk level ('high', 'medium', 'low') and reason
    """
    try:
        message_count = ChatMessage.query.filter_by(conversation_id=conversation.id).count()

        # Very short conversations
        if message_count <= 2:
            return ("high", "Very short conversation")

        # Has interest but no contact info
        has_interest = context_memory.get("package") or context_memory.get("square_meters")
        has_contact = context_memory.get("email") or context_memory.get("phone")

        if has_interest and not has_contact and message_count >= 5:
            return ("medium", "Interest shown but no contact info after 5 messages")

        # Long conversation without progress
        if message_count >= 10 and not has_contact:
            return ("high", "Long conversation without capturing lead")

        return ("low", "Normal engagement")

    except Exception as e:
        print(f"[Abandonment Risk] Error: {e}")
        return ("low", "Unknown")


def suggest_next_best_action(context_memory, lead_score):
    """
    AI recommendation for sales team: what to do next with this lead
    """
    actions = []

    # High-quality lead
    if lead_score >= 70:
        actions.append("🔥 HIGH PRIORITY - Call within 1 hour")
        if context_memory.get("package"):
            actions.append(f"Prepare quote for {context_memory.get('package')} package")
        if context_memory.get("square_meters"):
            actions.append(f"Calculate precise cost for {context_memory.get('square_meters')}m²")

    # Medium quality
    elif lead_score >= 40:
        actions.append("📧 Send follow-up email within 24h")
        if not context_memory.get("package"):
            actions.append("Share package comparison guide")
        if not context_memory.get("square_meters"):
            actions.append("Ask for apartment size for accurate quote")

    # Low quality
    else:
        actions.append("📱 Add to nurture campaign - monthly newsletter")
        actions.append("Send inspiration portfolio")

    # Location-based action
    if context_memory.get("city"):
        actions.append(f"Connect with local team in {context_memory.get('city')}")

    return " | ".join(actions) if actions else "Standard follow-up"


def check_booking_intent(message, context):
    """
    Sprawdź czy użytkownik chce umówić spotkanie
    Jeśli tak - zwróć link do Zencal z pre-filled danymi
    """
    booking_keywords = [
        "umów",
        "spotkanie",
        "konsultacj",
        "rezerwacj",
        "zapisa",
        "wizyt",
        "termin",
        "rozmow",
        "przedstawiciel",
    ]

    message_lower = message.lower()

    # Sprawdź czy użytkownik chce się umówić
    if any(keyword in message_lower for keyword in booking_keywords):
        try:
            from src.integrations.zencal_client import ZencalClient

            zencal = ZencalClient()

            # Pobierz dane z kontekstu jeśli dostępne
            name = context.get("name") if context else None
            email = context.get("email") if context else None

            booking_link = zencal.get_booking_link(client_name=name, client_email=email)

            return (
                f"Świetnie! Możesz umówić spotkanie z naszym ekspertem tutaj:\n\n"
                f"👉 {booking_link}\n\n"
                f"Wybierz dogodny termin, a my się skontaktujemy! 📅"
            )

        except Exception as e:
            print(f"[Booking Intent] Error: {e}")
            return None

    return None


def check_learned_faq(message):
    """
    Check if message matches any learned FAQ patterns
    Returns answer if match found, None otherwise
    """
    try:
        from src.models.faq_learning import LearnedFAQ

        message_lower = message.lower()

        # Get active learned FAQs
        learned_faqs = LearnedFAQ.query.filter_by(is_active=True).all()

        for faq in learned_faqs:
            # Simple keyword matching (can be improved with fuzzy matching)
            keywords = faq.question_pattern.lower().split()
            if any(keyword in message_lower for keyword in keywords):
                # Increment usage count
                faq.usage_count += 1
                db.session.commit()
                return faq.answer

        return None
    except Exception as e:
        print(f"[Learned FAQ] Error: {e}")
        return None


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
    """Sprawdź czy wiadomość dotyczy FAQ z użyciem fuzzy matching"""
    from difflib import SequenceMatcher

    message_lower = message.lower()

    def similarity(a, b):
        """Calculate similarity between two strings (0-1)"""
        return SequenceMatcher(None, a, b).ratio()

    # FAQ patterns with keywords and threshold
    faq_patterns = {
        "jak_dlugo_trwa": (
            ["jak długo", "ile trwa", "czas realizacji", "termin", "ile czasu", "czas wykończenia"],
            0.65,
        ),
        "czy_wlaczone_materialy": (
            ["materiały", "cena obejmuje", "co zawiera", "co dostanę", "co jest w cenie"],
            0.60,
        ),
        "mozna_dostosowac": (
            ["dostosować", "zmienić", "modyfikacja", "elastyczny", "zmiana", "personalizacja"],
            0.60,
        ),
        "gwarancja": (["gwarancja", "rękojmia", "reklamacja", "jak długa gwarancja"], 0.70),
        "dodatkowe_oplaty": (
            ["dodatkowe koszty", "dodatkowe opłaty", "ukryte koszty", "niespodzianki", "dopłaty"],
            0.65,
        ),
        "ile_kosztuje": (
            ["płatność", "zapłata", "koszt", "ile kosztuje", "cena", "wycena", "budżet"],
            0.55,
        ),
    }

    # Check each FAQ pattern with fuzzy matching
    best_match = None
    best_score = 0.0

    for faq_key, (keywords, threshold) in faq_patterns.items():
        for keyword in keywords:
            # Check if keyword appears in message (fast path)
            if keyword in message_lower:
                return FAQ.get(faq_key)

            # Fuzzy matching for typos and variations
            score = similarity(keyword, message_lower)
            if score > threshold and score > best_score:
                best_score = score
                best_match = faq_key

    if best_match:
        return FAQ.get(best_match)

    # Legacy fallback patterns (more strict checking)
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


@chatbot_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    """
    Submit user satisfaction feedback
    POST body: {session_id, rating (1-5), feedback_text (optional)}
    """
    try:
        data = request.get_json()
        session_id = data.get("session_id")
        rating = data.get("rating")
        feedback_text = data.get("feedback_text", "")

        if not session_id or not rating:
            return jsonify({"error": "session_id and rating are required"}), 400

        if rating not in [1, 2, 3, 4, 5]:
            return jsonify({"error": "rating must be between 1-5"}), 400

        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        # Save feedback
        conversation.user_satisfaction = rating
        conversation.feedback_text = feedback_text
        conversation.ended_at = datetime.now(timezone.utc)

        # Update lead if exists
        lead = Lead.query.filter_by(session_id=session_id).first()
        if lead:
            # Adjust lead score based on satisfaction
            if rating >= 4:
                lead.lead_score = min(lead.lead_score + 10, 100)
            elif rating <= 2:
                lead.lead_score = max(lead.lead_score - 10, 0)
            lead.last_interaction = datetime.now(timezone.utc)

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Feedback saved",
                    "rating": rating,
                    "thank_you": "Dziękujemy za opinię! 🙏",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/stats/leads", methods=["GET"])
def get_lead_stats():
    """
    Get lead statistics and quality metrics
    Requires admin key
    """
    admin_key = os.getenv("ADMIN_API_KEY")
    if admin_key:
        header = request.headers.get("X-ADMIN-API-KEY")
        if header != admin_key:
            return jsonify({"error": "Unauthorized"}), 401

    try:
        total_leads = Lead.query.count()
        confirmed_leads = Lead.query.filter_by(data_confirmed=True).count()
        high_quality_leads = Lead.query.filter(Lead.lead_score >= 70).count()
        medium_quality_leads = Lead.query.filter(
            Lead.lead_score >= 40, Lead.lead_score < 70
        ).count()
        low_quality_leads = Lead.query.filter(Lead.lead_score < 40).count()

        # Average scores
        avg_score = db.session.query(db.func.avg(Lead.lead_score)).scalar() or 0

        # Satisfaction stats
        total_feedback = ChatConversation.query.filter(
            ChatConversation.user_satisfaction.isnot(None)
        ).count()
        avg_satisfaction = (
            db.session.query(db.func.avg(ChatConversation.user_satisfaction)).scalar() or 0
        )

        # Recent high-priority leads (last 24h)
        from datetime import timedelta

        yesterday = datetime.now(timezone.utc) - timedelta(hours=24)
        recent_hot_leads = (
            Lead.query.filter(Lead.lead_score >= 70, Lead.created_at >= yesterday)
            .order_by(Lead.lead_score.desc())
            .limit(5)
            .all()
        )

        hot_leads_data = [
            {
                "name": lead.name,
                "score": lead.lead_score,
                "package": lead.interested_package,
                "email": lead.email,
                "next_action": lead.notes,
                "created_at": lead.created_at.isoformat(),
            }
            for lead in recent_hot_leads
        ]

        return (
            jsonify(
                {
                    "total_leads": total_leads,
                    "confirmed_leads": confirmed_leads,
                    "quality_distribution": {
                        "high (70-100)": high_quality_leads,
                        "medium (40-69)": medium_quality_leads,
                        "low (0-39)": low_quality_leads,
                    },
                    "average_lead_score": round(avg_score, 2),
                    "user_feedback": {
                        "total_responses": total_feedback,
                        "average_rating": round(avg_satisfaction, 2),
                    },
                    "hot_leads_24h": hot_leads_data,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/abandonment-alerts", methods=["GET"])
def get_abandonment_alerts():
    """
    Get conversations at risk of abandonment
    Requires admin key
    """
    admin_key = os.getenv("ADMIN_API_KEY")
    if admin_key:
        header = request.headers.get("X-ADMIN-API-KEY")
        if header != admin_key:
            return jsonify({"error": "Unauthorized"}), 401

    try:
        # Get active conversations (started in last 2 hours, not ended)
        from datetime import timedelta

        two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)

        active_conversations = (
            ChatConversation.query.filter(
                ChatConversation.started_at >= two_hours_ago,
                ChatConversation.ended_at.is_(None),
            )
            .order_by(ChatConversation.started_at.desc())
            .all()
        )

        alerts = []
        for conv in active_conversations:
            context = json.loads(conv.context_data or "{}")
            risk_level, reason = detect_abandonment_risk(conv, context)

            if risk_level in ["high", "medium"]:
                alerts.append(
                    {
                        "session_id": conv.session_id,
                        "risk_level": risk_level,
                        "reason": reason,
                        "started_at": conv.started_at.isoformat(),
                        "context": {
                            "name": context.get("name"),
                            "email": context.get("email"),
                            "phone": context.get("phone"),
                            "package": context.get("package"),
                            "square_meters": context.get("square_meters"),
                        },
                        "message_count": ChatMessage.query.filter_by(
                            conversation_id=conv.id
                        ).count(),
                    }
                )

        return (
            jsonify(
                {
                    "total_at_risk": len(alerts),
                    "high_risk": len([a for a in alerts if a["risk_level"] == "high"]),
                    "medium_risk": len([a for a in alerts if a["risk_level"] == "medium"]),
                    "alerts": alerts,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
        except Exception as e:
            print(f"[RODO] Warning: Failed to log audit entry: {e}")
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
        except Exception as e:
            print(f"[RODO] Warning: Failed to log cleanup audit entry: {e}")
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

        # Audit the export (if AuditLog table exists)
        try:
            audit = AuditLog(
                action="export",
                session_id=session_id,
                ip_address=request.remote_addr,
                details=f"Exported data for session {session_id}",
            )
            db.session.add(audit)
            db.session.commit()
        except Exception as e:
            # Rollback but don't fail the export if audit fails
            print(f"[RODO] Warning: Failed to log export audit entry: {e}")
            db.session.rollback()

        return jsonify(result), 200
    except Exception as e:
        db.session.rollback()
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


@chatbot_bp.route("/ab-tests/results", methods=["GET"])
def get_ab_test_results():
    """
    Get A/B testing results for follow-up questions
    Requires admin key
    """
    admin_key = os.getenv("ADMIN_API_KEY") or os.getenv("API_KEY")
    if admin_key:
        header = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
        if header != admin_key:
            return jsonify({"error": "Unauthorized"}), 401

    try:
        tests = FollowUpTest.query.all()
        results = []

        for test in tests:
            test_data = test.to_dict()

            # Statistical significance check (basic)
            total_shown = test.variant_a_shown + test.variant_b_shown
            if total_shown >= 100:  # Minimum sample size
                conv_a = test_data["stats"]["variant_a"]["conversion_rate"] or 0
                conv_b = test_data["stats"]["variant_b"]["conversion_rate"] or 0

                if abs(conv_a - conv_b) > 10:  # 10% difference threshold
                    winner = "A" if conv_a > conv_b else "B"
                    test_data["winner"] = winner
                    test_data["significance"] = "statistically significant"
                else:
                    test_data["winner"] = "inconclusive"
                    test_data["significance"] = "no significant difference"
            else:
                test_data["winner"] = "insufficient data"
                test_data["significance"] = f"need {100 - total_shown} more impressions"

            results.append(test_data)

        return jsonify({"tests": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/ab-tests/create", methods=["POST"])
def create_ab_test():
    """
    Create new A/B test for follow-up questions
    Requires admin key
    """
    admin_key = os.getenv("ADMIN_API_KEY") or os.getenv("API_KEY")
    if admin_key:
        header = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
        if header != admin_key:
            return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()

        test = FollowUpTest(
            question_type=data.get("question_type"),
            variant_a=data.get("variant_a"),
            variant_b=data.get("variant_b"),
            is_active=data.get("is_active", True),
        )

        db.session.add(test)
        db.session.commit()

        return jsonify({"message": "A/B test created", "test_id": test.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/competitive-intelligence", methods=["GET"])
def get_competitive_intelligence():
    """
    Get competitive intelligence insights from conversations
    Requires admin key
    """
    admin_key = os.getenv("ADMIN_API_KEY") or os.getenv("API_KEY")
    if admin_key:
        header = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
        if header != admin_key:
            return jsonify({"error": "Unauthorized"}), 401

    try:
        from datetime import timedelta

        # Get time range from query params (default: last 30 days)
        days = request.args.get("days", 30, type=int)
        since = datetime.now(timezone.utc) - timedelta(days=days)

        # Get all intel
        intel_records = CompetitiveIntel.query.filter(CompetitiveIntel.created_at >= since).all()

        # Aggregated stats
        total_mentions = len(intel_records)
        competitor_counts = {}
        intel_type_counts = {}
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        priority_counts = {"high": 0, "medium": 0, "low": 0}

        for intel in intel_records:
            # Count by competitor
            if intel.competitor_name:
                competitor_counts[intel.competitor_name] = (
                    competitor_counts.get(intel.competitor_name, 0) + 1
                )

            # Count by type
            intel_type_counts[intel.intel_type] = intel_type_counts.get(intel.intel_type, 0) + 1

            # Count by sentiment
            sentiment_counts[intel.sentiment] = sentiment_counts.get(intel.sentiment, 0) + 1

            # Count by priority
            priority_counts[intel.priority] = priority_counts.get(intel.priority, 0) + 1

        # Recent high-priority intel (last 10)
        recent_high_priority = (
            CompetitiveIntel.query.filter(CompetitiveIntel.priority == "high")
            .order_by(CompetitiveIntel.created_at.desc())
            .limit(10)
            .all()
        )

        return (
            jsonify(
                {
                    "summary": {
                        "total_mentions": total_mentions,
                        "date_range_days": days,
                        "competitor_mentions": competitor_counts,
                        "intel_types": intel_type_counts,
                        "sentiment_distribution": sentiment_counts,
                        "priority_distribution": priority_counts,
                    },
                    "recent_high_priority": [intel.to_dict() for intel in recent_high_priority],
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
