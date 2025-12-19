"""
Clean, stable chatbot core
No duplicate GPT calls, no test-call on init, proper DB fallback
"""
import json
import logging
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from flask import Blueprint, jsonify, request

from src.config.prompts import SYSTEM_PROMPT
from src.exceptions import ValidationError, ChatMessageTooLongError, BusinessException

from src.models.chatbot import (
    AuditLog,
    ChatConversation,
    ChatMessage,
    Lead,
    RodoConsent,
    db,
)

chatbot_bp = Blueprint("chatbot", __name__)

# ----------------------------
# OpenAI client (lazy, no test-call)
# ----------------------------

_openai_client = None

GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o-mini")
GPT_ENABLED = os.getenv("GPT_FALLBACK_ENABLED", "true").lower() == "true"


def get_openai_client():
    """Lazy init OpenAI client. NO test request here (cost + latency)."""
    global _openai_client

    if not GPT_ENABLED:
        return None

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.lower().startswith("test_"):
        logging.warning("OPENAI_API_KEY missing/test key – GPT disabled")
        return None

    if _openai_client is not None:
        return _openai_client

    try:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=api_key)
        logging.info("OpenAI client initialized (lazy)")
        return _openai_client
    except Exception as e:
        logging.error(f"OpenAI client init failed: {e}", exc_info=True)
        _openai_client = None
        return None


# ----------------------------
# In-memory fallback for context
# ----------------------------

_context_fallback: dict[str, dict] = {}


@dataclass
class ConversationState:
    conversation: Optional[ChatConversation]
    context: dict
    db_available: bool


def _load_conversation_and_context(session_id: str) -> ConversationState:
    """Load conversation+context. If DB fails, fallback to in-memory."""
    try:
        conv = ChatConversation.query.filter_by(session_id=session_id).first()
        if not conv:
            conv = ChatConversation(
                session_id=session_id,
                started_at=datetime.now(timezone.utc),
                context_data=json.dumps({}, ensure_ascii=False),
            )
            db.session.add(conv)
            db.session.commit()

        try:
            ctx = json.loads(conv.context_data or "{}")
            if not isinstance(ctx, dict):
                ctx = {}
        except Exception:
            ctx = {}

        return ConversationState(conversation=conv, context=ctx, db_available=True)
    except Exception as e:
        logging.warning(f"[DB FALLBACK] cannot load conversation: {e}")
        try:
            db.session.rollback()
        except Exception:
            pass
        return ConversationState(conversation=None, context=_context_fallback.get(session_id, {}), db_available=False)


def _save_context_and_message(
    state: ConversationState,
    session_id: str,
    user_message: str,
    bot_response: str,
) -> None:
    """Best-effort persistence. Never break the user flow."""
    # Always keep in-memory copy
    _context_fallback[session_id] = state.context

    if not state.db_available or not state.conversation:
        return

    try:
        conv_id = state.conversation.id
        # user message
        db.session.add(
            ChatMessage(
                conversation_id=conv_id,
                message=user_message,
                sender="user",
                timestamp=datetime.now(timezone.utc),
            )
        )
        # bot message
        db.session.add(
            ChatMessage(
                conversation_id=conv_id,
                message=bot_response,
                sender="bot",
                timestamp=datetime.now(timezone.utc),
            )
        )

        state.conversation.context_data = json.dumps(state.context, ensure_ascii=False)
        db.session.commit()
        return None
    except Exception as e:
        logging.warning(f"[DB] save failed (continuing): {e}")
        try:
            db.session.rollback()
        except Exceptionn:
            pass
        state.db_available = False


# ----------------------------
# Minimal "safe" context extraction hook
# ----------------------------

def extract_context_safe(user_message: str, existing: dict) -> dict:
    """Prefer your existing safe extractor if present, fallback to a strict minimal one."""
    try:
        from src.services.extract_context_safe import extract_context_safe as svc
        ctx = svc(user_message, existing)
    except Exception:
        ctx = dict(existing or {})
    
    text = user_message or ""

    # email
    m = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", text)
    if m:
        ctx["email"] = m.group(1).strip()

        # phone
        m = re.search(r"(\+?48\s?\d{3}\s?\d{3}\s?\d{3}|\d{3}\s?\d{3}\s?\d{3}|48\d{9})", text)
        if m:
            ctx["phone"] = m.group(1).strip()

        # square meters - CRITICAL: "50 m" = "50 square meters" in apartment context
        m = re.search(r"(\d{1,4})\s?(m2|m²|mkw|m(?!\w))", text, re.IGNORECASE)
        if m:
            try:
                sqm = int(m.group(1))
                if 10 <= sqm <= 500:
                    ctx["square_meters"] = sqm
            except ValueError:
                pass

        # budget
        m = re.search(r"(\d+[\s\d]*)(?:\s?tys|\s?000|\s?pln|\s?zł)", text, re.IGNORECASE)
        if m and "budget" not in ctx:
            raw = m.group(1).replace(" ", "")
            try:
                value = int(raw)
                if re.search(r"tys|tyś", text, re.IGNORECASE):
                    value *= 1000
                if 10000 <= value <= 10_000_000:
                    ctx["budget"] = value
            except ValueError:
                pass

    # Extract package from message (if not already set)
    if not ctx.get("package"):
        package = normalize_package(user_message)
        if package:
            ctx["package"] = package
            ctx["last_selected_package"] = package

    # Update conversation stage based on available data
    if ctx.get("square_meters") and ctx.get("package"):
        if not ctx.get("conversation_stage") or ctx.get("conversation_stage") == "DISCOVERY":
            ctx["conversation_stage"] = "QUOTE_READY"
    elif not ctx.get("conversation_stage"):
        ctx["conversation_stage"] = "DISCOVERY"

    return ctx


# ----------------------------
# Package prices (source of truth)
# ----------------------------

PACKAGE_PRICES = {
    "Express": 999,
    "Express Plus": 1199,
    "Comfort": 1499,
    "Premium": 1999,
    "Indywidualny": None,  # Custom pricing
}

PACKAGE_SYNONYMS = {
        "express": "Express",
    "podstawowy": "Express",
    "basic": "Express",
    "express plus": "Express Plus",
    "plus": "Express Plus",
    "expres plus": "Express Plus",
    "exp plus": "Express Plus",
    "standard": "Express Plus",
        "comfort": "Comfort",
    "komfort": "Comfort",
    "komfortowy": "Comfort",
        "premium": "Premium",
    "luxury": "Premium",
    "luksus": "Premium",
    "luksusowy": "Premium",
    "indywidualny": "Indywidualny",
    "custom": "Indywidualny",
    "na miarę": "Indywidualny",
}


def normalize_package(text: str) -> Optional[str]:
    """Normalize package name from user input to canonical form."""
    if not text:
        return None
    text_lower = text.lower().strip()
    # Direct match
    if text_lower in PACKAGE_SYNONYMS:
        return PACKAGE_SYNONYMS[text_lower]
    # Partial match
    for synonym, canonical in PACKAGE_SYNONYMS.items():
        if synonym in text_lower:
            return canonical
        return None


def calculate_quote(square_meters: int, package: str) -> Optional[dict]:
    """Calculate quote: total price and formatted string."""
    if not square_meters or not package:
        return None
    price_per_sqm = PACKAGE_PRICES.get(package)
    if not price_per_sqm:
        return None
    total = square_meters * price_per_sqm
    return {
        "square_meters": square_meters,
        "package": package,
        "price_per_sqm": price_per_sqm,
        "total": total,
        "formatted": f"{total:,} zł".replace(",", " "),
    }


# ----------------------------
# Short message handler (CRITICAL - before FAQ/GPT)
# ----------------------------

def handle_short_message(user_message: str, context: dict) -> Optional[str]:
    """
    Handle short messages (1-2 words) in context.
    Must be called BEFORE FAQ/GPT to prevent "plus" -> "podaj metraż" bug.
    """
    if not user_message:
        return None

    msg = user_message.strip().lower()
    msg_len = len(msg.split())

    # Only handle very short messages (1-3 words, max 15 chars)
    if msg_len > 3 or len(msg) > 15:
        return None

    # Package selection: "plus", "premium", "comfort", "express"
    package_normalized = normalize_package(msg)
    if package_normalized:
        sqm = context.get("square_meters")
        last_package = context.get("last_selected_package") or context.get("package")

        # Update context
        context["package"] = package_normalized
        context["last_selected_package"] = package_normalized
        context["last_intent"] = "package_selection"

        # If we have square meters - calculate and respond immediately
        if sqm:
            quote = calculate_quote(sqm, package_normalized)
            if quote:
                price_per_sqm = PACKAGE_PRICES[package_normalized]
                # Check if we have contact data - if yes, propose consultation immediately
                has_contact = context.get("email") or context.get("phone")
                name = context.get("name", "")
                
                if has_contact:
                    # We have everything - propose consultation
                    response = (
                        f"Dziękuję {name + ', ' if name else ''}mam wszystkie dane: **{sqm} m²**, pakiet: **{package_normalized}**.\n\n"
                        f"Wstępna wycena: **{quote['formatted']}** ({sqm} × {price_per_sqm} zł/m²).\n\n"
                        f"Wyślemy Ci szczegółową wycenę na email. Czy chcesz, aby nasz ekspert oddzwonił dziś po 16:00, by omówić szczegóły?"
                    )
                else:
                    response = (
                        f"Jasne — **{package_normalized}**. "
                        f"Przy **{sqm} m²** wychodzi ok. **{quote['formatted']}** "
                        f"({sqm} × {price_per_sqm} zł/m²).\n\n"
                        f"To wstępna wycena; ostatecznie zależy od zakresu i materiałów.\n\n"
                        f"Chcesz porównać z innymi pakietami czy doprecyzować zakres (łazienka/kuchnia/elektryka)?"
                    )
                context["last_quoted_price"] = quote["total"]
                context["last_price_calc"] = quote
                context["conversation_stage"] = "QUOTE_GIVEN"
                return response

        # No square meters yet
        response = (
            f"OK, zapisuję **{package_normalized}**. "
            f"Podaj proszę metraż (m²), a policzę wstępnie koszt."
        )
        context["conversation_stage"] = "DISCOVERY"
        return response

    # Confirmation: "tak", "ok", "jasne"
    if msg in ["tak", "ok", "okay", "jasne", "zgadza się", "zgodne"]:
        last_question = context.get("last_question_type")
        if last_question == "data_confirmation":
            # User confirmed data - move forward
            sqm = context.get("square_meters")
            package = context.get("package")
            if sqm and package:
                quote = calculate_quote(sqm, package)
                if quote:
                    response = (
                        f"Super! Mam: **{sqm} m²**, pakiet: **{package}**. "
                        f"Wstępnie: **{quote['formatted']}** ({sqm} × {PACKAGE_PRICES[package]} zł/m²).\n\n"
                        f"Chcesz umówić bezpłatną konsultację, żeby doprecyzować zakres?"
                    )
                    context["conversation_stage"] = "QUOTE_GIVEN"
                    return response
        elif last_question == "booking_yes":
            # User wants booking
            try:
                from src.integrations.zencal_client import ZencalClient
                booking_link = ZencalClient().get_booking_link(
                    context.get("name"), context.get("email")
                )
            except Exception:   booking_link = os.getenv(
                    "ZENCAL_BOOKING_URL", "https://zencal.io/novahouse/konsultacja"
                )
            context["booking_intent_detected"] = True
            context["conversation_stage"] = "BOOKING"
            return f"Super — zarezerwuj bezpłatną konsultację tutaj: {booking_link}"

    # Negative: "nie", "zmień"
    if msg in ["nie", "zmień", "zmien", "inny"]:
        # User wants to change something - ask what
        return "Jasne. Co chcesz zmienić? (pakiet/metraż/budżet)"

    return None


# ----------------------------
# FAQ + booking routing (clean)
# ----------------------------

def check_faq(user_message: str) -> Optional[str]:
    try:
        from src.services.faq_service import faq_service
        return faq_service.check_faq(user_message)
    except Exception:
        return None


def check_learned_faq(user_message: str) -> Optional[str]:
    try:
        from src.services.faq_service import faq_service
        return faq_service.check_learned_faq(user_message)
    except Exception:
        return None

        return None
def check_booking_intent(user_message: str, context: dict) -> Optional[str]:
    msg = (user_message or "").lower()
    if not any(k in msg for k in ["umów", "konsult", "spotkan", "rezerw", "termin"]):
        return None

    try:
        from src.integrations.zencal_client import ZencalClient
        booking_link = ZencalClient().get_booking_link(context.get("name"), context.get("email"))
    except Exception:
        booking_link = os.getenv("ZENCAL_BOOKING_URL", "https://zencal.io/novahouse/konsultacja")

    context["booking_intent_detected"] = True
    return f"Super — zarezerwuj bezpłatną konsultację tutaj: {booking_link}"


def get_default_response(_: str) -> str:
    return (
        "Dzięki! Napisz proszę: metraż + miasto + orientacyjny budżet, "
        "a przygotuję dopasowanie pakietu i widełki kosztów."
    )


# ----------------------------
# Single GPT call (no duplicates)
# ----------------------------

def call_gpt(user_message: str, context: dict, history: list[dict] | None = None) -> Optional[str]:
    client = get_openai_client()
    if not client:
        return None

    # Build context-aware memory prompt
    memory_lines = []
    if context.get("square_meters"):
        memory_lines.append(f"Metraż: {context['square_meters']} m²")
    if context.get("city"):
        memory_lines.append(f"Miasto: {context['city']}")
    if context.get("budget"):
        memory_lines.append(f"Budżet: {context['budget']} zł")
    if context.get("package"):
        memory_lines.append(f"Pakiet: {context['package']}")
        # Add price calculation if we have both
        if context.get("square_meters"):
            quote = calculate_quote(context["square_meters"], context["package"])
            if quote:
                memory_lines.append(f"Wycena: {quote['formatted']} ({quote['square_meters']} × {quote['price_per_sqm']} zł/m²)")
    if context.get("name"):
        memory_lines.append(f"Imię: {context['name']}")

    # CRITICAL: Add rule about not asking for data we already have
    context_rules = ""
    if memory_lines:
        context_rules = "\n\nDane podane przez klienta (NIE PYTAJ PONOWNIE):\n" + "\n".join(memory_lines)
        context_rules += "\n\n⚠️ WAŻNE: Jeśli masz metraż/pakiet/miasto - NIE pytaj o nie ponownie. Użyj ich do odpowiedzi."
        
        # CRITICAL: If we have square meters, ALWAYS calculate and show quote
        if context.get("square_meters") and not context.get("package"):
            context_rules += "\n\n🚨 KRYTYCZNE: Masz metraż - ZAWSZE przelicz i pokaż wycenę dla 3-4 pakietów (Express, Express Plus, Comfort, Premium)."
        elif context.get("square_meters") and context.get("package"):
            quote = calculate_quote(context["square_meters"], context["package"])
            if quote:
                context_rules += f"\n\n🚨 KRYTYCZNE: Masz metraż {context['square_meters']} m² i pakiet {context['package']} - wycena: {quote['formatted']}. Użyj tej informacji w odpowiedzi!"

    # Add conversation stage context
    stage = context.get("conversation_stage", "DISCOVERY")
    if stage == "QUOTE_READY" or stage == "QUOTE_GIVEN":
        context_rules += "\n\nKlient ma już wycenę - możesz proponować następne kroki (konsultacja, porównanie pakietów, doprecyzowanie zakresu)."
    
    # CRITICAL: If we have contact data + square meters + package, propose consultation immediately
    has_contact = context.get("email") or context.get("phone")
    has_sqm = context.get("square_meters")
    has_package = context.get("package")
    if has_contact and has_sqm and has_package:
        context_rules += "\n\n🎯 KRYTYCZNE: Masz wszystkie dane (kontakt + metraż + pakiet) - ZAWSZE zaproponuj konsultację, NIE pytaj ponownie o pakiety/metraż!"

    messages = [{"role": "system", "content": SYSTEM_PROMPT + context_rules}]
    if history:
        messages.extend(history[-8:])  # krótko i tanio
    messages.append({"role": "user", "content": user_message})

    try:
        resp = client.chat.completions.create(
                        model=GPT_MODEL,
                        messages=messages,
            max_tokens=250,  # Reduced for faster responses
            temperature=0.6,
            timeout=30.0,
        )
        text = resp.choices[0].message.content
        if text and text.strip():
            # Sanity check before returning
            text_lower = text.lower()
            sanity_blocklist = [
                "nie wiem", "jako model", "placeholder", "instrukcja",
                "system prompt", "nie mogę", "nie potrafię", "jako ai"
            ]
            for phrase in sanity_blocklist:
                if phrase in text_lower:
                    logging.warning(f"[GPT] Sanity check failed - detected: {phrase}")
                    # Return safe fallback
                    return (
                        "Przepraszam, nie jestem pewien odpowiedzi. "
                        "Możesz doprecyzować pytanie lub skontaktować się z nami bezpośrednio?"
                    )
            return text.strip()
        return None
    except Exception as e:
        logging.error(f"[GPT] call failed: {e}", exc_info=True)
        return None


def load_history_for_gpt(conversation: Optional[ChatConversation], limit: int = 12) -> list[dict]:
    if not conversation:
        return []
    try:
        msgs = (
                        ChatMessage.query.filter_by(conversation_id=conversation.id)
                        .order_by(ChatMessage.timestamp.asc())
            .limit(limit)
                        .all()
                    )
        out = []
        for m in msgs:
            role = "assistant" if m.sender == "bot" else "user"
            out.append({"role": role, "content": m.message})
        return out
    except Exception:
        return []


# ----------------------------
# Lead scoring (clean + predictable)
# ----------------------------

def calculate_lead_score(context: dict, message_count: int) -> int:
    score = 0
    score += 10 if context.get("name") else 0
    score += 10 if context.get("email") else 0
    score += 10 if context.get("phone") else 0
    score += 10 if context.get("city") else 0
    score += 10 if context.get("square_meters") else 0
    score += 15 if context.get("package") else 0
    score += 15 if context.get("budget") else 0
    score += min(message_count * 2, 10) if score > 0 else 0
    return min(score, 100)


def suggest_next_best_action(context: dict, lead_score: int) -> str:
    if lead_score >= 70 and (context.get("email") or context.get("phone")):
        return "HIGH PRIORITY: oddzwoń w 1h, wyślij dopasowaną ofertę, zaproponuj konsultację."
    if lead_score >= 50:
        return "Follow-up w 24h: propozycja + konsultacja."
    if lead_score >= 30:
        return "Nurture: case studies + delikatny follow-up."
    return "Nurture: newsletter + lekkie follow-upy."


# ----------------------------
# Post-processing bot response (replace Pan/Pani with name, prevent redundant questions)
# ----------------------------

def postprocess_bot_response_text(bot_response: str, context_memory: dict | None = None) -> str:
    """Post-process bot response to improve conversational style and prevent redundant questions."""
    if not bot_response or not context_memory:
        return bot_response

    try:
        # 1) Replace "Pan/Pani" with user's name if known
        name = context_memory.get("name")
        if name:
            safe_name = name.strip()
            if "Pan/Pani" in bot_response:
                bot_response = bot_response.replace("Pan/Pani", safe_name)

        # 2) CRITICAL: Never ask for data we already have
        sqm = context_memory.get("square_meters")
        package = context_memory.get("package")
        city = context_memory.get("city")

        # Forbidden questions patterns
        forbidden_patterns = []
        if sqm:
            forbidden_patterns.extend([
                "podaj metraż", "proszę o metraż", "jaki metraż", "ile metrów",
                "podaj m²", "proszę m²", "jaki m²", "ile m²"
            ])
        if package:
            forbidden_patterns.extend([
                "jaki pakiet", "wybierz pakiet", "który pakiet", "podaj pakiet"
            ])
        if city:
            forbidden_patterns.extend([
                "w jakim mieście", "podaj miasto", "jaki miasto"
            ])

        # Check and replace forbidden questions
        bot_lower = bot_response.lower()
        for pattern in forbidden_patterns:
            if pattern in bot_lower:
                # Replace with context-aware response
                if sqm and "metraż" in pattern or "m²" in pattern:
                    bot_response = (
                        f"Rozumiem, że mieszkanie ma {sqm} m². "
                        f"Na tej podstawie mogę doprecyzować wycenę i czas realizacji."
                    )
                elif package and "pakiet" in pattern:
                    bot_response = (
                        f"Masz wybrany pakiet **{package}**. "
                        f"Chcesz porównać z innymi czy doprecyzować zakres?"
                    )
                break

        # 3) Sanity check - filter placeholder/instruction text
        sanity_blocklist = [
            "nie wiem", "jako model", "placeholder", "instrukcja",
            "system prompt", "nie mogę", "nie potrafię"
        ]
        for phrase in sanity_blocklist:
            if phrase in bot_lower:
                # Replace with safe fallback
                bot_response = (
                    "Przepraszam, nie jestem pewien. "
                    "Możesz doprecyzować pytanie lub skontaktować się z nami bezpośrednio?"
                )
                break

    except Exception:
        pass

    return bot_response


# ----------------------------
# Main flow (short and sane)
# ----------------------------

def process_chat_message(user_message: str, session_id: str) -> dict:
    state = _load_conversation_and_context(session_id)

    # Extract/update context
    state.context = extract_context_safe(user_message, state.context)

    # History (optional)
    history = load_history_for_gpt(state.conversation)

    # Routing with priority (CRITICAL: short_message_handler BEFORE FAQ/GPT)
    # 1. Booking intent
    bot_response = check_booking_intent(user_message, state.context)
    # 2. Short message handler (MUST be before FAQ/GPT to handle "plus", "premium", "tak")
    if not bot_response:
        bot_response = handle_short_message(user_message, state.context)
    # 3. Learned FAQ
    if not bot_response:
        bot_response = check_learned_faq(user_message)
    # 4. Standard FAQ
    if not bot_response:
        bot_response = check_faq(user_message)
    # 5. GPT (with context-aware prompt)
    if not bot_response:
        bot_response = call_gpt(user_message, state.context, history)
    # 6. Fallback
    if not bot_response:
        bot_response = get_default_response(user_message)

    # Post-process response (replace Pan/Pani, prevent redundant questions)
    bot_response = postprocess_bot_response_text(bot_response, state.context)

    # Persist (best effort)
    _save_context_and_message(state, session_id, user_message, bot_response)

    # Lead score (cheap)
    message_count = 0
    if state.db_available and state.conversation:
        try:
            message_count = ChatMessage.query.filter_by(conversation_id=state.conversation.id).count()
        except Exception:
            message_count = 0

    lead_score = calculate_lead_score(state.context, message_count)
    next_action = suggest_next_best_action(state.context, lead_score)

    return {
            "response": bot_response,
            "session_id": session_id,
        "conversation_id": state.conversation.id if state.conversation else None,
        "context": state.context,
            "lead_score": lead_score,
            "next_best_action": next_action,
        }


# ----------------------------
# Flask endpoints
# ----------------------------

@chatbot_bp.route("/health", methods=["GET"])
def chatbot_health():
    return jsonify({"status": "healthy", "service": "chatbot"}), 200


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    # Rate limiting handled by middleware in main.py
    """Clean chat endpoint - no duplicate GPT calls, proper error handling"""
    payload = request.get_json(silent=True) or {}

    from src.utils.validators import validate_chat_payload
    try:
        user_message, session_id = validate_chat_payload(payload)
    except (ValidationError, ChatMessageTooLongError):
        raise

    if not session_id:
        session_id = str(uuid.uuid4())

    # Check IP blacklist
    try:
        from src.services.ip_blacklist import ip_blacklist
        ip_address = request.remote_addr or "unknown"
        if ip_blacklist.is_blacklisted(ip_address):
            return jsonify({
                "error": "ip_blacklisted",
                "message": "Your IP has been temporarily blocked due to rate limit violations"
            }), 403
    except Exception:
        pass  # File open
    
    # Check minimum interval between messages
    try:
        from src.services.rate_limiter import ensure_rate_limiter
        limiter_instance = ensure_rate_limiter()
        min_interval = int(os.getenv("MIN_MESSAGE_INTERVAL_SECONDS", "1"))
        allowed, wait_seconds = limiter_instance.check_minimum_interval(
            f"session:{session_id}",
            min_interval
        )
        if not allowed:
            return jsonify({
                "error": "message_too_fast",
                "message": f"Please wait {wait_seconds} seconds before sending another message",
                "retry_after": wait_seconds
            }), 429
    except Exception:
        pass  # File open

    try:
        from src.services.monitoring import track_request, MetricsService
        with track_request("/chat"):
            response_data = process_chat_message(user_message, session_id)
            MetricsService.increment_conversation("success")
    except BusinessException:
        raise  # Let business exceptions propagate
    except Exception:
        from src.services.monitoring import MetricsService, capture_exception
        MetricsService.increment_error(500)
        MetricsService.increment_conversation("error")
        capture_exception(e, extra={"session_id": session_id})
        logging.exception("Error in chat endpoint")
        raise

    return jsonify(
        {
            "response": response_data["response"],
            "session_id": response_data["session_id"],
            "conversation_id": response_data["conversation_id"],
            "context": response_data["context"],
            "lead_score": response_data["lead_score"],
            "next_best_action": response_data["next_best_action"],
            "alerts": [],
        }
    )


# ----------------------------
# Additional endpoints (preserved for compatibility)
# ----------------------------

@chatbot_bp.route("/history/<session_id>", methods=["GET"])
def get_history(session_id):
    """Get conversation history"""
    try:
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        messages = (
            ChatMessage.query.filter_by(conversation_id=conversation.id)
            .order_by(ChatMessage.timestamp.asc())
            .all()
        )

        return jsonify({
            "session_id": session_id,
            "conversation_id": conversation.id,
                    "messages": [
                        {
                            "sender": msg.sender,
                    "message": msg.message,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                        }
                        for msg in messages
            ],
        })
    except Exception as e:
        logging.error(f"Error getting history: {e}", exc_info=True)
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

        # Usuń z fallback cache
        if session_id in _context_fallback:
            del _context_fallback[session_id]

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
            logging.warning(f"[RODO] Warning: Failed to log audit entry: {e}", exc_info=True)
            db.session.rollback()

        return (
            jsonify(
                {"success": True, "message": "Wszystkie Twoje dane zostały usunięte zgodnie z RODO"}
            ),
            200,
        )

    except Exception:
        db.session.rollback()
        logging.error(f"Error deleting user data: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# Keep other endpoints for backward compatibility (can be moved to separate files later)
@chatbot_bp.route("/rodo-consent", methods=["POST"])
def rodo_consent():
    """RODO consent endpoint - preserved for compatibility"""
    try:
        data = request.get_json()
        session_id = data.get("session_id")
        consent_type = data.get("consent_type", "general")
        
        consent = RodoConsent(
            session_id=session_id,
            consent_type=consent_type,
            granted=True,
            granted_at=datetime.now(timezone.utc),
        )
        db.session.add(consent)
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/rodo-consent/<session_id>", methods=["GET"])
def get_rodo_consent(session_id):
    """Get RODO consent for session"""
    try:
        consent = RodoConsent.query.filter_by(session_id=session_id).first()
        if not consent:
            return jsonify({"consent": False}), 200
        return jsonify({"consent": consent.granted}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/consents", methods=["GET"])
def get_all_consents():
    """Get all consents (admin)"""
    try:
        from src.routes.chatbot import _check_admin_key
        admin_check = _check_admin_key()
        if admin_check:
            return admin_check
        
        consents = RodoConsent.query.all()
        return jsonify({
            "consents": [
                {
                    "session_id": c.session_id,
                    "consent_type": c.consent_type,
                    "granted": c.granted,
                    "granted_at": c.granted_at.isoformat() if c.granted_at else None,
                }
                for c in consents
            ]
        }), 200
    except Exception:
        jsonify({"error": str(e)}), 500


def _check_admin_key():
    """Check admin API key"""
    admin_key = os.getenv("ADMIN_API_KEY")
    if not admin_key:
        return None
    header = request.headers.get("X-API-KEY")
    if header == admin_key:
        return None
    return (jsonify({"error": "Unauthorized"}), 401)


@chatbot_bp.route("/audit", methods=["GET"])
def get_audit_logs():
    """Get audit logs (admin)"""
    try:
        admin_check = _check_admin_key()
        if admin_check:
            return admin_check
        
        logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
        return jsonify({
            "logs": [
                {
                    "action": log.action,
                    "session_id": log.session_id,
                    "ip_address": log.ip_address,
                    "timestamp": log.timestamp.isoformat() if log.timestamp else None,
                    "details": log.details,
                }
                for log in logs
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/audit/cleanup", methods=["POST"])
def cleanup_audit_logs():
    """Cleanup old audit logs (admin)"""
    try:
        admin_check = _check_admin_key()
        if admin_check:
            return admin_check
        
        from datetime import timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(days=90)
        deleted = AuditLog.query.filter(AuditLog.timestamp < cutoff).delete()
        db.session.commit()
        return jsonify({"deleted": deleted}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@chatbot_bp.route("/export-data/<session_id>", methods=["GET"])
def export_user_data(session_id):
    """Export user data (RODO Art. 15)"""
    try:
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        messages = (
                ChatMessage.query.filter_by(conversation_id=conversation.id)
                .order_by(ChatMessage.timestamp.asc())
                .all()
            )

        context = json.loads(conversation.context_data or "{}")

        return jsonify({
            "session_id": session_id,
            "conversation_id": conversation.id,
            "started_at": conversation.started_at.isoformat() if conversation.started_at else None,
            "context": context,
            "messages": [
                {
                    "sender": msg.sender,
                    "message": msg.message,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                }
                for msg in messages
            ],
        }), 200
    except Exception as e:
        logging.error(f"Error exporting data: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
