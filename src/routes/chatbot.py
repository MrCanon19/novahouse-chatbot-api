genai = None  # Dummy dla testów
# Pozwala na patchowanie genai w testach

import json
import logging
import os
import re
import uuid
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from src.exceptions import ValidationError, ChatMessageTooLongError, BusinessException

# Lazy load OpenAI to optimize cold start
OPENAI_AVAILABLE = False
_openai_client = None

# GPT Model selection (env configurable)
# OPTIMIZED FOR COST: gpt-4o-mini is the best balance of quality/price
# Pricing (as of 2024): 
#   - gpt-4o-mini: $0.15/$0.60 per 1M tokens (input/output) - BEST VALUE
#   - gpt-4o: $2.50/$10.00 per 1M tokens - 16x more expensive
#   - gpt-3.5-turbo: $0.50/$1.50 per 1M tokens - worse Polish support
# Recommendation: gpt-4o-mini for 95% of cases, escalate to gpt-4o only if needed
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o-mini")  # Default: gpt-4o-mini (optimized for cost)


def get_openai_client():
    """Lazy load OpenAI client"""
    global OPENAI_AVAILABLE, _openai_client
    if _openai_client is None:
        try:
            from openai import OpenAI

            _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            OPENAI_AVAILABLE = True
            print(f"✅ OpenAI client initialized with model: {GPT_MODEL}")
        except ImportError:
            OPENAI_AVAILABLE = False
            print("⚠️  openai package not installed - GPT disabled")
    return _openai_client


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
from src.config.prompts import SYSTEM_PROMPT

chatbot_bp = Blueprint("chatbot", __name__)

# Import limiter (initialized in main.py, decorated here)
from src.main import limiter


def calculate_lead_score(context_memory, message_count):
    """Lead score tuned for test expectations and runtime heuristics."""
    base_score = 0
    if context_memory.get("name"):
        base_score += 10
    if context_memory.get("email"):
        base_score += 10
    if context_memory.get("phone"):
        base_score += 10
    if context_memory.get("city"):
        base_score += 10
    if context_memory.get("square_meters"):
        base_score += 10
    if context_memory.get("package"):
        base_score += 15

    score = base_score
    if base_score > 0:
        score += min(message_count * 2, 10)
    return min(score, 100)


def extract_context(message: str, existing_context: dict | None = None):
    """Safe extractor with regex fallback for tests."""
    original_context = dict(existing_context or {})
    context = dict(existing_context or {})

    # Regex/validator extraction to satisfy tests without over-normalizing
    text = message or ""
    ctx = context

    from src.services.context_validator import ContextValidator

    # Email
    email_match = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", text)
    if email_match:
        candidate_email = email_match.group(1).strip()
        valid, value, _ = ContextValidator.validate_email(candidate_email)
        if valid:
            ctx["email"] = value

    # Name (prefer introduction pattern, fall back to last capitalized pair)
    preferred_name = None
    intro_match = re.search(
        r"(?:jestem|nazywam się|mam na imię|to ja)\s+([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?:\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)+)",
        text,
        re.IGNORECASE,
    )
    if intro_match:
        preferred_name = intro_match.group(1).strip()
    else:
        capitalized_pairs = re.findall(
            r"[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+",
            text,
        )
        if capitalized_pairs:
            preferred_name = capitalized_pairs[-1].strip()

    if preferred_name:
        valid, value, _ = ContextValidator.validate_name(preferred_name)
        if valid and (not ctx.get("name") or ctx["name"].lower().startswith("jestem")):
            ctx["name"] = value

    # Phone (capture formatted raw phone to satisfy formatting expectations)
    phone_match = re.search(
        r"(\+?48\s?\d{3}\s?\d{3}\s?\d{3}|\d{3}\s?\d{3}\s?\d{3}|48\d{9})",
        text,
    )
    if phone_match:
        ctx["phone"] = phone_match.group(1).strip()

    # City (improved recognition - all Polish cities)
    # Pattern 1: "jestem z Wrocławia" / "mieszkam w Warszawie" / "z Wrocławia"
    city_match = re.search(r"\b(?:z|ze|w|we|mieszkam|jestem|pochodzę)\s+([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?:\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)*)", text, re.IGNORECASE)
    if city_match:
        candidate_city = city_match.group(1).strip()
        try:
            from src.utils.polish_cities import PolishCities

            # Try to normalize using cities database
            normalized = PolishCities.normalize_city_name(candidate_city)
            if normalized:
                candidate_city = normalized
            
            # Check if city is in database (all Polish cities)
            city_variants = [candidate_city, candidate_city.title(), candidate_city.capitalize()]
            recognized_city = None
            for variant in city_variants:
                if variant in PolishCities.CITIES:
                    recognized_city = variant
                    break
                if variant in PolishCities.ALL_POLISH_CITIES_GUS:
                    recognized_city = variant
                    break
            
            if recognized_city:
                valid, value, _ = ContextValidator.validate_city(recognized_city)
                if valid:
                    ctx["city"] = value
            else:
                # Fallback: try to clean up common endings
                lower_city = candidate_city.lower()
                if lower_city.endswith("iu") and len(candidate_city) > 5:
                    candidate_city = candidate_city[:-2]
                elif lower_city.endswith("u") and len(candidate_city) > 5:
                    candidate_city = candidate_city[:-1]
                elif lower_city.endswith("ia") and len(candidate_city) > 5:
                    candidate_city = candidate_city  # Keep as is
                
                valid, value, _ = ContextValidator.validate_city(candidate_city)
                if valid:
                    ctx["city"] = value
        except Exception as e:
            logging.warning(f"Error recognizing city: {e}")
            # Fallback to old logic
            if candidate_city.lower().startswith("warszaw"):
                candidate_city = "Warszawa"
            valid, value, _ = ContextValidator.validate_city(candidate_city)
            if valid:
                ctx["city"] = value

    # Budget (numbers with tys/PLN)
    budget_match = re.search(r"(\d+[\s\d]*)(?:\s?tys|\s?000|\s?pln|\s?zł)", text, re.IGNORECASE)
    if budget_match and not ctx.get("budget"):
        raw = budget_match.group(1).replace(" ", "")
        try:
            value = int(raw)
            if re.search(r"tys|tyś", text, re.IGNORECASE):
                value *= 1000
            if 50000 <= value <= 5000000:
                ctx["budget"] = value
        except ValueError:
            pass

    # Square meters
    sqm_match = re.search(r"(\d{1,4})\s?(m2|m²|mkw|metr|metry|metrów)", text, re.IGNORECASE)
    if sqm_match:
        try:
            sqm_val = int(sqm_match.group(1))
            valid, value, _ = ContextValidator.validate_square_meters(sqm_val)
            if valid:
                ctx["square_meters"] = value
        except ValueError:
            pass

    # Package keywords
    package_keywords = {
        "express": "Express",
        "express+": "Express+",
        "comfort": "Comfort",
        "premium": "Premium",
        "indywid": "Indywidualny",
    }
    lower_text = text.lower()
    for kw, val in package_keywords.items():
        if kw in lower_text and not ctx.get("package"):
            ctx["package"] = val
            break

    # Preserve previously validated name if new extraction is too weak (e.g., "Tak")
    original_name = original_context.get("name")
    if original_name and ctx.get("name") and ctx["name"] != original_name:
        if len(ctx["name"].split()) < 2:
            ctx["name"] = original_name

    return ctx


def generate_conversation_summary(messages, context_memory):
    summary = "Konwersacja z chatbotem:\n"
    for msg in messages:
        text = getattr(msg, "message", getattr(msg, "text", ""))
        sender = getattr(msg, "sender", "user") or "user"
        summary += f"{sender.capitalize()}: {text}\n"
    summary += "\nZebrane dane:\n"
    for key, value in context_memory.items():
        summary += f"- {key}: {value}\n"
    return summary


def suggest_next_best_action(context_memory, lead_score):
    """Sugeruj najlepsze następne działanie na podstawie lead score i danych"""
    if lead_score >= 70 and (context_memory.get("email") or context_memory.get("phone")):
        return "HIGH PRIORITY: Call within 1 hour and send tailored offer via email. Suggest booking consultation."
    if lead_score >= 50:
        return "Follow-up via email within 24h with a tailored proposal. Offer free consultation."
    if lead_score >= 30:
        return "Nurture via newsletter and light touch follow-ups. Share case studies."
    return "Nurture via newsletter and light touch follow-ups."


def check_learned_faq(user_message: str):
    """Safe wrapper around learned FAQ lookup."""
    try:
        from src.services.faq_service import faq_service

        return faq_service.check_learned_faq(user_message)
    except Exception:
        return None


def check_faq(user_message: str):
    """FAQ lookup with defensive fallback."""
    try:
        from src.services.faq_service import faq_service

        answer = faq_service.check_faq(user_message)
        if answer:
            return answer
    except Exception:
        pass

    # Lightweight manual fallback for common intents
    lower_msg = (user_message or "").lower()
    if "ile" in lower_msg and "czas" in lower_msg:
        return (
            "Projekt + realizacja zajmuje zwykle około 6-8 tygodni, w zależności od zakresu prac."
        )
    return None


def should_ask_for_confirmation(context_memory, conversation):
    """Simple heuristic for confirmation without breaking tests if unavailable."""
    try:
        has_contact = context_memory.get("name") and (
            context_memory.get("email") or context_memory.get("phone")
        )
        return bool(has_contact and not getattr(conversation, "awaiting_confirmation", False))
    except Exception:
        return False


def check_data_confirmation_intent(user_message: str):
    """Stub confirmation intent detector to avoid runtime errors."""
    msg = (user_message or "").lower()
    import re

    if any(keyword in msg for keyword in ["potwierdz", "potwierdzam", "tak"]):
        return "confirm"
    if re.search(r"\bnie\b", msg) or any(
        keyword in msg for keyword in ["popraw", "zmien", "zmiana", "edytuj"]
    ):
        return "edit"
    return None


def detect_competitive_intelligence(user_message: str, session_id: str, context_memory: dict):
    """Safe wrapper; no-op if competitor service unavailable."""
    try:
        from src.services.competitor_service import detect_competitive_intelligence as detector

        return detector(user_message, session_id, context_memory)
    except Exception:
        return None


def generate_follow_up_question(context_memory, user_message, bot_response, conversation):
    """Safe wrapper for optional follow-up automation."""
    try:
        from src.services.followup_automation import generate_follow_up_question as generator

        return generator(context_memory, user_message, bot_response, conversation)
    except Exception:
        return None


def get_default_response(user_message: str):
    """Graceful fallback when no intent/FAQ matched."""
    return (
        "Dziękuję za wiadomość! Jak mogę pomóc w wykończeniu Twojego mieszkania? "
        "Możesz zapytać o ofertę, pakiety lub terminy realizacji."
    )


def check_booking_intent(user_message: str, context_memory: dict):
    """Detect booking intent and return a booking prompt with link when matched."""
    message_lower = (user_message or "").lower()
    keywords = [
        "umów",
        "spotkan",
        "termin",
        "rezerw",
        "konsult",
        "wizy",
        "booking",
        "chcę się spotkać",
        "chciałbym się spotkać",
        "chciałabym się spotkać",
        "spotkajmy się",
        "kiedy możemy się spotkać",
        "gdy możemy się spotkać",
    ]

    if not any(k in message_lower for k in keywords):
        return None

    try:
        from src.integrations.zencal_client import ZencalClient

        zencal = ZencalClient()
        booking_link = zencal.get_booking_link(
            context_memory.get("name"), context_memory.get("email")
        )
    except Exception as e:
        print(f"[Zencal] Error getting booking link: {e}")
        booking_link = os.getenv("ZENCAL_BOOKING_URL", "https://zencal.io/novahouse/konsultacja")

    context_memory["booking_intent_detected"] = True
    
    # Jeśli mamy imię, użyj go
    name = context_memory.get("name", "")
    if name:
        from src.utils.polish_declension import PolishDeclension
        declined_name = PolishDeclension.decline_full_name(name)
        return f"Świetnie {declined_name}! 🎉 Zarezerwuj bezpłatną konsultację tutaj: {booking_link}\n\nTo zajmie tylko 2 minuty - wybierz dogodny termin, a nasz ekspert skontaktuje się z Tobą!"
    else:
        return f"Świetnie! 🎉 Zarezerwuj bezpłatną konsultację tutaj: {booking_link}\n\nTo zajmie tylko 2 minuty - wybierz dogodny termin, a nasz ekspert skontaktuje się z Tobą!"


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

        # Extract and update context from user message (with safeguards)
        try:
            from src.services.extract_context_safe import extract_context_safe

            context_memory = extract_context_safe(user_message, context_memory)
        except ImportError:
            # Fallback to legacy extract_context if safe version not available
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
        db.session.commit()
        
        # Update session activity
        try:
            from src.services.session_timeout import session_timeout_service
            session_timeout_service.update_activity(session_id)
        except Exception as e:
            logging.warning(f"Failed to update session activity: {e}")

        # Detect if the current message is an introduction (to prioritize GPT routing)
        intro_keywords = ["jestem", "nazywam się", "mam na imię", "to ja", "cześć jestem"]
        is_introduction = any(k in user_message.lower() for k in intro_keywords)

        # 1. Check if user wants to book a meeting
        bot_response = check_booking_intent(user_message, context_memory)

        # 2. Check learned FAQs (higher priority - learned from real users)
        if not bot_response:
            bot_response = check_learned_faq(user_message)

        # 3. Then check standard FAQ (skip if this is a self-introduction)
        if not bot_response and not is_introduction:
            bot_response = check_faq(user_message)

        # 4. Jeśli nie znaleziono w FAQ, ZAWSZE użyj AI (OpenAI GPT) - PRIORYTET!
        if not bot_response:
            client = ensure_openai_client()
            if client:
                try:
                    # Pobierz historię konwersacji (limit zwiększony do 20)
                    message_history_limit = int(os.getenv("MESSAGE_HISTORY_LIMIT", "20"))
                    history = (
                        ChatMessage.query.filter_by(conversation_id=conversation.id)
                        .order_by(ChatMessage.timestamp.desc())
                        .limit(message_history_limit)
                        .all()
                    )

                    context = "\n".join(
                        [
                            f"{'User' if msg.sender == 'user' else 'Bot'}: {msg.message}"
                            for msg in reversed(history[:-1])  # Exclude current message
                        ]
                    )

                    # Add memory context with proper name declension and city recognition
                    memory_prompt = ""
                    if context_memory:
                        from src.utils.polish_declension import PolishDeclension
                        from src.utils.polish_cities import PolishCities

                        memory_items = []
                        if context_memory.get("name"):
                            name = context_memory["name"]
                            declined_name = PolishDeclension.decline_full_name(name)
                            is_polish = PolishDeclension.is_polish_name(name.split()[0])
                            gender = PolishDeclension.detect_gender(name.split()[0])

                            # Add both forms for GPT reference
                            memory_items.append(
                                f"Imię: {name} (wołacz: {declined_name}, polskie: {is_polish}, płeć: {gender})"
                            )
                        if context_memory.get("city"):
                            city = context_memory["city"]
                            # Check if city is recognized in Polish cities database
                            city_variants = [city, city.title(), city.lower(), city.capitalize()]
                            recognized_city = None
                            for variant in city_variants:
                                if variant in PolishCities.CITIES:
                                    recognized_city = variant
                                    break
                                # Check in ALL_POLISH_CITIES_GUS
                                if variant in PolishCities.ALL_POLISH_CITIES_GUS:
                                    recognized_city = variant
                                    break
                            
                            if recognized_city:
                                memory_items.append(f"Miasto: {recognized_city} (działamy w tym mieście!)")
                            else:
                                memory_items.append(f"Miasto: {city}")
                        if context_memory.get("square_meters"):
                            memory_items.append(f"Metraż: {context_memory['square_meters']}m²")
                        if context_memory.get("budget"):
                            memory_items.append(f"Budżet: {context_memory['budget']} zł")
                        if context_memory.get("package"):
                            memory_items.append(f"Interesujący pakiet: {context_memory['package']}")
                        if memory_items:
                            memory_prompt = "\n\nZapamiętane info o kliencie:\n" + "\n".join(
                                memory_items
                            ) + "\n\nWAŻNE: Używaj imienia naturalnie (co 2-3 wiadomości), zapamiętuj miasto i metraż, przeliczaj ceny automatycznie!"

                    # COST OPTIMIZATION: Check cache first for similar questions
                    try:
                        from src.middleware.cache import cache
                        import hashlib
                        # Create cache key from normalized user message (ignore case, whitespace)
                        normalized_msg = user_message.lower().strip()
                        cache_key = f"gpt_response:{hashlib.md5(normalized_msg.encode()).hexdigest()}"
                        cached_response = cache.get(cache_key)
                        if cached_response:
                            print(f"[GPT CACHE HIT] Using cached response for: {user_message[:50]}...")
                            bot_response = cached_response
                        else:
                            print(f"[OpenAI GPT] Przetwarzanie: {user_message[:50]}...")
                            messages = [
                                {"role": "system", "content": SYSTEM_PROMPT + memory_prompt},
                                {
                                    "role": "user",
                                    "content": f"Context:\n{context}\n\nUser: {user_message}",
                                },
                            ]
                            # OPTIMIZED FOR COST: Reduced max_tokens from 500 to 350 (saves ~30% on output costs)
                            # Most chatbot responses are 200-300 tokens, 350 is sufficient
                            response = client.chat.completions.create(
                                model=GPT_MODEL,
                                messages=messages,
                                max_tokens=350,  # Optimized: was 500, saves ~30% on output costs
                                temperature=0.6,  # Optimized: was 0.7, slightly more focused responses
                            )
                            bot_response = response.choices[0].message.content
                            # Cache response for 1 hour (3600s) - common questions get cached
                            cache.set(cache_key, bot_response, ttl=3600)
                            print(
                                f"[OpenAI GPT] Response: {bot_response[:100] if bot_response else 'EMPTY'}..."
                            )
                    except ImportError:
                        # Cache not available, use GPT directly
                        print(f"[OpenAI GPT] Przetwarzanie: {user_message[:50]}...")
                        messages = [
                            {"role": "system", "content": SYSTEM_PROMPT + memory_prompt},
                            {
                                "role": "user",
                                "content": f"Context:\n{context}\n\nUser: {user_message}",
                            },
                        ]
                        response = client.chat.completions.create(
                            model=GPT_MODEL,
                            messages=messages,
                            max_tokens=350,
                            temperature=0.6,
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

        # Add proactive booking suggestion if we have data
        if context_memory.get("_booking_suggestion") and not context_memory.get("booking_intent_detected"):
            booking_link = context_memory.pop("_booking_suggestion")
            name = context_memory.get("name", "")
            if name:
                from src.utils.polish_declension import PolishDeclension
                declined_name = PolishDeclension.decline_full_name(name)
                booking_text = f"\n\n💡 {declined_name}, chcesz umówić bezpłatną konsultację? Nasz ekspert dopasuje idealny pakiet do Twojego projektu! Zarezerwuj tutaj: {booking_link}"
            else:
                booking_text = f"\n\n💡 Chcesz umówić bezpłatną konsultację? Nasz ekspert dopasuje idealny pakiet do Twojego projektu! Zarezerwuj tutaj: {booking_link}"
            bot_response = bot_response + booking_text

        # Track A/B test response (if user responded to follow-up question)
        if conversation.followup_variant and len(user_message) > 3:
            # TODO: Implement track_ab_test_response function
            pass  # track_ab_test_response(conversation)

        # Check if we just collected enough data to ask for confirmation
        should_confirm = should_ask_for_confirmation(context_memory, conversation)
        print(
            f"[CONFIRMATION CHECK] should_confirm={should_confirm}, context={context_memory}, awaiting={conversation.awaiting_confirmation}"
        )
        if should_confirm:
            conversation.awaiting_confirmation = True
            # Use lead creation strategy method or build inline
            confirmation_parts = []
            if context_memory.get("name"):
                confirmation_parts.append(f"Imię: {context_memory['name']}")
            if context_memory.get("email"):
                confirmation_parts.append(f"Email: {context_memory['email']}")
            if context_memory.get("phone"):
                confirmation_parts.append(f"Telefon: {context_memory['phone']}")
            if context_memory.get("city"):
                confirmation_parts.append(f"Miasto: {context_memory['city']}")
            if confirmation_parts:
                confirmation_msg = "Potwierdzam dane:\n" + "\n".join(confirmation_parts)
                bot_response = f"{bot_response}\n\n{confirmation_msg}"
                print("[CONFIRMATION] Added confirmation message to response")

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

        # Check if we have enough data to create lead
        has_enough_data_for_lead = context_memory.get("name") and (
            context_memory.get("email") or context_memory.get("phone")
        )

        if confirmation_intent == "confirm" and has_enough_data_for_lead and not existing_lead:
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
                        print(f"Lead created in Monday.com: {lead.name}, score: {lead_score}")

                    # Alert dla leadów o wysokim priorytecie
                    if lead_score >= 70:
                        try:
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
                            print(f"ALERT: High-priority lead: {lead.name}, score: {lead_score}")
                        except Exception as e:
                            print(f"Failed to send high-priority alert: {e}")

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

        # Fallback: Auto-create lead if enough data (no confirmation asked)
        # Create lead automatically if we have contact data OR high lead score
        elif not conversation.awaiting_confirmation and not existing_lead:
            try:
                has_contact_data = (
                    context_memory.get("name")
                    and (context_memory.get("email") or context_memory.get("phone"))
                )
                
                # Also create lead if we have project data (metraż/budżet) even without contact
                # This allows us to capture leads earlier
                has_project_data = context_memory.get("square_meters") or context_memory.get("budget")
                
                # Calculate lead score first to decide
                message_count = ChatMessage.query.filter_by(
                    conversation_id=conversation.id
                ).count()
                lead_score = calculate_lead_score(context_memory, message_count)
                
                # Create lead if:
                # 1. We have contact data (name + email/phone)
                # 2. OR we have project data (metraż/budżet) AND lead score >= 30
                should_create_lead = has_contact_data or (has_project_data and lead_score >= 30)

                if should_create_lead:
                    from src.integrations.monday_client import MondayClient

                    # message_count and lead_score already calculated above

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

        message_count = ChatMessage.query.filter_by(conversation_id=conversation.id).count()
        lead_score = calculate_lead_score(context_memory, message_count)
        next_action = suggest_next_best_action(context_memory, lead_score)

        return {
            "response": bot_response,
            "session_id": session_id,
            "conversation_id": conversation.id,
            "context": context_memory,
            "lead_score": lead_score,
            "next_best_action": next_action,
        }

    except SQLAlchemyError as e:
        logging.error(f"Database error in chat processing: {e}", exc_info=True)
        db.session.rollback()
        # Try to continue without database (graceful degradation)
        try:
            # Return a basic response without saving to database
            return {
                "response": "Cześć! Mogę pomóc Ci z informacjami o pakietach wykończeniowych NovaHouse. O co chciałbyś zapytać?",
                "session_id": session_id,
                "conversation_id": None,
            }
        except Exception as fallback_error:
            logging.error(f"Fallback also failed: {fallback_error}")
            return {
                "response": "Przepraszam, problem z bazą danych. Spróbuj ponownie za chwilę.",
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

# Lazy initialize OpenAI client
openai_client = None
AI_PROVIDER = None


def ensure_openai_client():
    """Ensure OpenAI client is initialized (lazy loading)"""
    global openai_client, AI_PROVIDER
    gpt_enabled = os.getenv("GPT_FALLBACK_ENABLED", "true").lower() == "true"
    if not gpt_enabled:
        print("⚠️  GPT_FALLBACK_ENABLED=false – skipping GPT client init")
        return None

    # Always try to get client (even if already initialized, to ensure it's working)
    if OPENAI_API_KEY and not OPENAI_API_KEY.lower().startswith("test_"):
        client = get_openai_client()
        if client:
            openai_client = client
            AI_PROVIDER = "openai"
            if not openai_client:  # Only print if first time
                print("✅ OpenAI GPT-4o-mini enabled (proven & reliable)")
            return openai_client
        else:
            print("⚠️  No AI configured - set OPENAI_API_KEY")
            return None
    else:
        print(f"⚠️  OPENAI_API_KEY missing/placeholder (key starts with: {OPENAI_API_KEY[:10] if OPENAI_API_KEY else 'None'}) – GPT disabled")
        return None


if MONDAY_API_KEY:
    print("✅ Monday.com API key loaded")
else:
    print("⚠️  No Monday.com API key - set MONDAY_API_KEY")


@chatbot_bp.route("/chat", methods=["POST"])
@limiter.limit(lambda: os.getenv("CHAT_RATE_LIMIT", "30 per minute"))
def chat():
    """Handle chat messages via REST API (NEW: with state machine, validation, rate limiting)"""
    # Check IP blacklist
    from src.services.ip_blacklist import ip_blacklist
    
    ip_address = request.remote_addr or "unknown"
    if ip_blacklist.is_blacklisted(ip_address):
        return jsonify({
            "error": "ip_blacklisted",
            "message": "Your IP has been temporarily blocked due to rate limit violations"
        }), 403
    
    # Check minimum interval between messages
    from src.services.rate_limiter import ensure_rate_limiter
    
    payload = request.get_json(silent=True) or {}
    session_id = payload.get("session_id") or "unknown"
    
    try:
        limiter = ensure_rate_limiter()
        min_interval = int(os.getenv("MIN_MESSAGE_INTERVAL_SECONDS", "1"))
        allowed, wait_seconds = limiter.check_minimum_interval(
            f"session:{session_id}",
            min_interval
        )
        if not allowed:
            return jsonify({
                "error": "message_too_fast",
                "message": f"Please wait {wait_seconds} seconds before sending another message",
                "retry_after": wait_seconds
            }), 429
    except Exception as e:
        # Fail open if limiter unavailable
        logging.warning(f"Minimum interval check failed: {e}")
    
    payload = request.get_json(silent=True) or {}

    # Validate payload using validator
    from src.utils.validators import validate_chat_payload
    
    try:
        user_message, session_id = validate_chat_payload(payload)
    except (ValidationError, ChatMessageTooLongError) as e:
        # These are business errors, will be handled by global error handler
        raise
    
    # Generate session_id if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    try:
        from src.services.monitoring import track_request, MetricsService, capture_exception
        
        with track_request("/chat"):
            response_data = process_chat_message(user_message, session_id)
            MetricsService.increment_conversation("success")
    except Exception as e:  # pragma: no cover - defensive
        # Let business exceptions propagate to global handler
        from src.exceptions import BusinessException
        if isinstance(e, BusinessException):
            raise
        
        from src.services.monitoring import MetricsService, capture_exception
        from flask import g
        
        MetricsService.increment_error(500)
        MetricsService.increment_conversation("error")
        capture_exception(e, extra={"session_id": session_id})
        
        logging.exception("Error in chat endpoint")
        
        # Re-raise to be caught by global handler
        raise

    return jsonify(
        {
            "response": response_data.get("response"),
            "session_id": session_id,
            "conversation_id": response_data.get("conversation_id"),
            "context": response_data.get("context"),
            "lead_score": response_data.get("lead_score"),
            "next_best_action": response_data.get("next_best_action"),
            "alerts": response_data.get("alerts", []),
        }
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
