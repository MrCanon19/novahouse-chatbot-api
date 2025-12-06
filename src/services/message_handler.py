"""
Refactored Message Handler
Modular, clean, with state machine and validation
"""

import json
import logging
import os
import re
import time
import unicodedata
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

from src.models.chatbot import ChatConversation, ChatMessage, CompetitiveIntel, Lead, db
from src.services.context_validator import ContextValidator
from src.services.conversation_state_machine import ConversationStateMachine
from src.services.llm.engine import run_llm
from src.services.multi_turn_dialog import multi_turn_dialog
from src.services.proactive_suggestions import proactive_suggestions
from src.services.rate_limiter import conversation_limiter
from src.services.extract_context_safe import extract_context_safe
from src.services.retry_handler import failed_operations, retry_monday_api, retry_openai_api
from src.services.sentiment_service import sentiment_service
from src.services.session_timeout import session_timeout_service
from src.services.summarization_service import summarization_service


class MessageHandler:
    """Handles chat message processing with state management"""

    def __init__(self):
        self.validator = ContextValidator()
        # Per-session GPT call limiter to prevent runaway costs
        self._gpt_call_window_sec = int(os.getenv("GPT_CALL_WINDOW_SEC", "60"))
        self._gpt_calls_per_window = int(os.getenv("GPT_CALLS_PER_WINDOW", "5"))
        self._gpt_call_tracker: Dict[str, Dict[str, float]] = {}
        self._gpt_enabled = os.getenv("GPT_FALLBACK_ENABLED", "true").lower() == "true"
        # GPT metrics tracking
        self._gpt_drop_count = 0
        self._gpt_success_count = 0
        self._gpt_rate_limit_drops = 0
        self._gpt_placeholder_key_drops = 0

    def process_message(self, user_message: str, session_id: str) -> Dict:
        """
        Main entry point for message processing

        Returns:
            dict with response, session_id, conversation_id, state
        """
        try:
            # 0. Normalize user input for better extraction (preserve original for history)
            normalized_message = self._normalize_input(user_message)

            # 1. Rate limiting & spam detection
            spam_check = self._check_spam(session_id, normalized_message)
            if spam_check:
                return {"error": spam_check, "response": "Proszę zwolnić tempo wiadomości."}

            # 2. Find or create conversation
            conversation = self._get_or_create_conversation(session_id)

            # 3. Update session activity (for timeout detection)
            session_timeout_service.update_activity(session_id)

            # 4. Load and validate context
            context_memory = json.loads(conversation.context_data or "{}")

            # 4b. PERSISTENT MEMORY: Check if returning customer
            returning_customer = self._restore_returning_customer_context(
                session_id, context_memory
            )
            if returning_customer:
                print(
                    f"[PersistentMemory] ✓ Returning customer detected: {returning_customer.get('name')}"
                )

            # 5. Get message history for multi-turn dialog (last 30 messages for context)
            # Strategy: Keep recent messages for anaphora resolution (a co z tem?, a w warszawie?)
            # Limit: 30 messages = ~15 user-bot exchanges (enough for most conversations)
            MAX_HISTORY_SIZE = 30
            messages = ChatMessage.query.filter_by(conversation_id=conversation.id).all()
            # Keep only last MAX_HISTORY_SIZE messages
            messages = (
                messages[-MAX_HISTORY_SIZE:] if len(messages) > MAX_HISTORY_SIZE else messages
            )
            message_history = [{"sender": m.sender, "message": m.message} for m in messages]

            # 6. Resolve references in multi-turn dialog (a srebrnego?, a w warszawie?)
            resolved_message = multi_turn_dialog.resolve_references(
                normalized_message, context_memory, message_history, session_id
            )
            if resolved_message != normalized_message:
                print(f"[MultiTurn] Resolved '{user_message}' -> '{resolved_message}'")
                normalized_message = resolved_message

            # 7. Initialize state machine
            state_machine = ConversationStateMachine()
            current_state = state_machine.determine_state(context_memory)
            state_machine.current_state = current_state

            # 8. Extract context from message
            context_memory = self._extract_and_validate_context(normalized_message, context_memory)

            # 8b. Heuristics: enrich context if we have key signals
            # Pass both original and normalized message - use original for name extraction
            context_memory = self._enrich_context_with_heuristics(
                normalized_message, context_memory, user_message
            )

            # 9. Analyze sentiment in real-time
            sentiment_analysis = sentiment_service.analyze_message_sentiment(
                normalized_message, session_id
            )

            # Save user message
            self._save_message(conversation.id, user_message, "user")

            # 10. Generate response based on state
            bot_response, follow_up = self._generate_response(
                normalized_message,
                context_memory,
                conversation,
                state_machine,
                sentiment_analysis,
            )

            # 11. Handle state transitions
            new_state = state_machine.determine_state(context_memory)
            if new_state != current_state:
                success, error = state_machine.transition(new_state)
                if not success:
                    print(f"[StateMachine] Transition failed: {error}")

            # 12. Save bot response
            self._save_message(conversation.id, bot_response, "bot")

            # 13. Generate proactive suggestions
            suggestions = proactive_suggestions.get_suggestions(
                new_state, context_memory, user_message
            )

            # 14. Update conversation context with summary
            # Note: For summary, we can use all messages (not limited to MAX_HISTORY_SIZE)
            # because context_data is stored separately and summary is for analytics
            messages_for_summary = ChatMessage.query.filter_by(
                conversation_id=conversation.id
            ).all()
            message_history = [
                {"sender": m.sender, "message": m.message} for m in messages_for_summary
            ]

            # Calculate conversation duration
            duration_seconds = 0
            if conversation.started_at and messages_for_summary:
                from datetime import timezone

                latest_message_time = max(m.timestamp for m in messages_for_summary)
                # Ensure both datetimes are aware
                started_at = (
                    conversation.started_at.replace(tzinfo=timezone.utc)
                    if conversation.started_at.tzinfo is None
                    else conversation.started_at
                )
                latest_time = (
                    latest_message_time.replace(tzinfo=timezone.utc)
                    if latest_message_time.tzinfo is None
                    else latest_message_time
                )
                duration_seconds = int((latest_time - started_at).total_seconds())

            conversation_summary = summarization_service.generate_summary(
                context_memory, message_history, duration_seconds
            )

            conversation.context_data = json.dumps(context_memory)
            conversation.conversation_summary = conversation_summary
            db.session.commit()

            # Try to auto-create lead if enough data is available
            lead_info = self._try_create_lead(conversation, context_memory, session_id)

            return {
                "response": bot_response + (f"\n\n{follow_up}" if follow_up else ""),
                "session_id": session_id,
                "conversation_id": conversation.id,
                "state": state_machine.current_state.value,
                "sentiment": sentiment_analysis,
                "suggestions": suggestions,
                "typing_indicator": True,  # Signal to frontend
                "summary": summarization_service.generate_short_summary(context_memory),
                "lead_created": lead_info is not None,
                "lead_info": lead_info,
            }

        except Exception as e:
            import logging
            import traceback

            logger = logging.getLogger(__name__)
            logger.error(f"[MessageHandler] Critical error: {e}", exc_info=True)
            print(f"[MessageHandler] Error: {e}")
            print(f"[MessageHandler] Traceback: {traceback.format_exc()}")

            # Critical: dispose connection pool if DB error
            if "OperationalError" in str(type(e)) or "server closed" in str(e).lower():
                try:
                    logger.warning("🔄 Disposing connection pool due to DB error")
                    db.engine.dispose()
                except Exception as dispose_err:
                    logger.warning(f"Failed to dispose pool: {dispose_err}")

            db.session.rollback()
            try:
                from src.utils.telegram_alert import send_telegram_alert

                send_telegram_alert(f"Błąd produkcyjny w chatbocie: {str(e)[:200]}")
            except Exception as alert_exc:
                print(f"[Telegram Alert] Failed: {alert_exc}")
            return {
                "error": "internal_error",
                "response": "Przepraszam, wystąpił problem techniczny. Możesz spróbować ponownie lub zadzwonić: +48 502 274 453",
            }

    def _check_spam(self, session_id: str, message: str) -> Optional[str]:
        """Check for spam patterns - skip rate limiting for important intents"""
        # Skip rate limiting for booking and important business intents (also contact info)
        important_keywords = [
            "umów",
            "spotkanie",
            "konsultacj",
            "rezerwacj",
            "zapisa",
            "wizyt",
            "telefon",
            "email",
            "kontakt",
        ]
        if any(keyword in message.lower() for keyword in important_keywords):
            print(f"[Rate Limiter] SKIPPED for important intent: {message[:30]}")
            return None

        conversation_limiter.add_message(session_id, message)
        is_spam, reason = conversation_limiter.is_spam(session_id, message)
        if is_spam:
            print(f"[Spam] Detected for {session_id}: {reason}")
            return f"Spam detected: {reason}"
        return None

    def _get_or_create_conversation(self, session_id: str) -> ChatConversation:
        """Find or create conversation"""
        from sqlalchemy.exc import OperationalError

        logger = logging.getLogger(__name__)
        max_retries = 2

        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            conversation = ChatConversation(
                session_id=session_id,
                started_at=datetime.now(timezone.utc),
                context_data=json.dumps({}),
            )

            retry_count = 0
            while retry_count < max_retries:
                try:
                    db.session.add(conversation)
                    db.session.flush()
                    return conversation
                except OperationalError as e:
                    retry_count += 1
                    db.session.rollback()
                    error_msg = str(e).lower()

                    if "server closed" in error_msg or "connection" in error_msg:
                        if retry_count < max_retries:
                            wait_time = 1 * retry_count
                            logger.warning(
                                f"⚠️ DB error creating conversation (attempt {retry_count}/{max_retries}), "
                                f"retrying in {wait_time}s"
                            )
                            time.sleep(wait_time)
                            db.engine.dispose()
                        else:
                            logger.error(
                                f"❌ Failed to create conversation after {max_retries} attempts"
                            )
                            raise
                    else:
                        logger.error(
                            f"❌ Non-retryable error creating conversation: {str(e)[:150]}"
                        )
                        raise
        return conversation

    def _normalize_input(self, message: str) -> str:
        """Lowercase, strip emoji/punctuation noise, normalize meters/budget formats."""
        text = message.lower()
        text = text.replace(",", ".")
        # remove common emoji/symbols (keep polish letters and digits)
        text = re.sub(r"[^0-9a-ząćęłńóśżź\s\.\-]+", " ", text)
        # normalize metraż tokens
        text = re.sub(r"m2|metr(?:ow|ów)?|metr(?:y)?", " m2 ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _strip_accents(self, text: str) -> str:
        """Remove accents for fuzzy intent checks (greetings with typos)."""
        normalized = unicodedata.normalize("NFKD", text)
        return "".join(ch for ch in normalized if not unicodedata.combining(ch))

    def _levenshtein(self, a: str, b: str) -> int:
        """Small Levenshtein distance for short tokens."""
        if a == b:
            return 0
        if not a:
            return len(b)
        if not b:
            return len(a)
        # Early exit if lengths differ too much
        if abs(len(a) - len(b)) > 2:
            return 3

        prev_row = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            curr_row = [i]
            for j, cb in enumerate(b, 1):
                cost = 0 if ca == cb else 1
                curr_row.append(
                    min(
                        curr_row[-1] + 1,  # insertion
                        prev_row[j] + 1,  # deletion
                        prev_row[j - 1] + cost,  # substitution
                    )
                )
            prev_row = curr_row
        return prev_row[-1]

    def _is_greeting(self, message: str) -> bool:
        """Detect greetings with minor typos (czesc, cześć, hejj, witaj)."""
        base = self._strip_accents(message.lower())
        base_clean = re.sub(r"[^a-z\s]", " ", base)
        tokens = base_clean.split()
        greetings = [
            "czesc",
            "czescie",
            "czes",
            "cześć",
            "hej",
            "heja",
            "hejka",
            "siema",
            "witaj",
            "witam",
            "dzień",
            "dzien",
            "dobry",
        ]

        for token in tokens:
            if token in greetings:
                return True
            for g in greetings:
                if self._levenshtein(token, g) <= 1:
                    return True

        # Multi-word greetings like "dzien dobry"
        if "dzien dobry" in base_clean or "dzien dob" in base_clean:
            return True
        if "dz" in tokens and "dobry" in tokens:
            return True

        return False

    def _build_greeting_response(self, context_memory: Dict) -> str:
        """Friendly welcome that nudges for key data."""
        prompts = []
        if not context_memory.get("name"):
            prompts.append("Jak masz na imię?")

        missing = self._get_missing_fields(context_memory)
        if "city" in missing:
            prompts.append("Podaj miasto inwestycji.")
        if "property_type" in missing:
            prompts.append("To mieszkanie czy dom?")
        if "square_meters" in missing:
            prompts.append("Ile m2 ma nieruchomość?")
        if "budget" in missing:
            prompts.append("Jaki budżet zakładasz (może być orientacyjny)?")

        ask = " ".join(prompts) if prompts else "W czym mogę pomóc?"
        return f"Cześć! Jestem asystentem NovaHouse. {ask}"

    def _enrich_context_with_heuristics(
        self, message: str, context: Dict, original_message: str = None
    ) -> Dict:
        """Heuristic extraction: budget (zł/pln), metraż, miasto, typ, name.
        Uses original_message for name extraction (before lowercasing).
        """
        updated = dict(context)

        # Use original message for name extraction (has proper capitalization)
        name_extraction_text = original_message or message

        # Name: Try to extract single name or "imię nazwisko" format (only if not already set)
        if not updated.get("name"):
            name_patterns = [
                r"(?:jestem|nazwam się|mam na imię|to ja|cześć jestem)\s+([A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+(?:\s+[A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)?)",
                r"^([A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+\s+[A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)$",  # "Jan Kowalski"
                r"^([A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)$",  # Single name "Michał"
            ]
            for pattern in name_patterns:
                name_match = re.search(pattern, name_extraction_text, re.IGNORECASE)
                if name_match:
                    extracted_name = name_match.group(1).strip()
                    if len(extracted_name) >= 2 and extracted_name[0].isupper():
                        updated["name"] = extracted_name
                        break

        # Budget: e.g. 200000, 200k, 200 tys
        budget_match = re.search(r"(\d+[\.]?\d*)\s*(k|tys)?\s*(zł|pln)?", message)
        if budget_match and not updated.get("budget"):
            try:
                val = float(budget_match.group(1))
                if budget_match.group(2):
                    val = val * 1000
                updated["budget"] = int(val)
            except Exception:
                pass

        # Square meters: number followed by m2, metr, metrów, metorow, m², etc.
        sqm_match = re.search(r"(\d+[\.]?\d*)\s*(m2|m²|metr|metrów|metorow|mkw)", message)
        if sqm_match and not updated.get("square_meters"):
            try:
                updated["square_meters"] = int(float(sqm_match.group(1)))
            except Exception:
                pass

        # Property type - only extract if it's in context of a property info question
        # Don't extract from generic questions like "obejrzeć mieszkanie online"
        if not updated.get("property_type"):
            # Look for "dom" or "mieszkanie" in context of property decisions (e.g., "to dom czy mieszkanie", "ile metrów ma dom")
            # or when paired with budget/metraż info
            if re.search(
                r"\bdom\b.*(?:metr|m2|m²|budżet|budzet|ile|jaki|który)", message, re.IGNORECASE
            ) or re.search(
                r"(?:metr|m2|m²|budżet|budzet|ile|jaki|który).*\bdom\b", message, re.IGNORECASE
            ):
                updated["property_type"] = "dom"
            elif re.search(
                r"\bmieszkani\w*\b.*(?:metr|m2|m²|budżet|budzet|ile|jaki|który)",
                message,
                re.IGNORECASE,
            ) or re.search(
                r"(?:metr|m2|m²|budżet|budzet|ile|jaki|który).*\bmieszkani\w*\b",
                message,
                re.IGNORECASE,
            ):
                updated["property_type"] = "mieszkanie"
            # Also catch direct answers like "dom", "mieszkanie" alone or "to dom", "to mieszkanie"
            elif re.search(r"^\s*(?:to\s+)?dom\s*$", message, re.IGNORECASE):
                updated["property_type"] = "dom"
            elif re.search(r"^\s*(?:to\s+)?mieszkani\w*\s*$", message, re.IGNORECASE):
                updated["property_type"] = "mieszkanie"

        # City (limited list of major cities)
        if not updated.get("city"):
            cities = [
                "warszawa",
                "krakow",
                "kraków",
                "wroclaw",
                "wrocław",
                "poznan",
                "poznań",
                "gdansk",
                "gdańsk",
                "gdynia",
                "szczecin",
                "lublin",
                "lodz",
                "łódź",
            ]
            for city in cities:
                if city in message:
                    updated["city"] = city
                    break

        return updated

    def _extract_and_validate_context(self, message: str, existing_context: Dict) -> Dict:
        """Extract context from message and validate"""
        updated_context = extract_context_safe(message, existing_context)

        # Validate and sanitize
        is_valid, sanitized, errors = self.validator.validate_context(updated_context)

        if errors:
            print(f"[Validation] Errors: {errors}")
            # Keep original values if validation failed; drop newly provided invalid fields
            for field in list(errors.keys()):
                if field in updated_context and field in existing_context:
                    updated_context[field] = existing_context[field]
                else:
                    updated_context.pop(field, None)

        # Merge sanitized values
        updated_context.update(sanitized)

        return updated_context

    def _generate_response(
        self,
        user_message: str,
        context_memory: Dict,
        conversation: ChatConversation,
        state_machine: ConversationStateMachine,
        sentiment_analysis: Dict = None,
    ) -> Tuple[str, Optional[str]]:
        """
        Generate bot response based on state and message

        Returns:
            (bot_response, follow_up_question)
        """
        from src.routes.chatbot import (
            check_booking_intent,
            check_data_confirmation_intent,
            check_faq,
            check_learned_faq,
            generate_follow_up_question,
        )

        # Check for data confirmation
        confirmation_intent = check_data_confirmation_intent(user_message)
        if confirmation_intent == "confirm" and conversation.awaiting_confirmation:
            return self._handle_confirmation(conversation, context_memory)

        # Check for escalation due to negative sentiment
        if sentiment_analysis and sentiment_analysis.get("should_escalate"):
            return self._handle_escalation(sentiment_analysis, conversation)

        # Friendly greeting if user starts with a hello (even with typos)
        # Check if it's a short greeting without much context
        is_short_greeting = self._is_greeting(user_message) and len(user_message.split()) <= 3
        has_minimal_context = not any(
            [context_memory.get("name"), context_memory.get("email"), context_memory.get("phone")]
        )

        if is_short_greeting and has_minimal_context:
            greeting_response = self._build_greeting_response(context_memory)
            # Strip bold just in case
            greeting_response = greeting_response.replace("**", "")
            return greeting_response, None

        # Response hierarchy (GPT FIRST for intelligent responses)
        bot_response = None

        # 1. Booking intent (highest priority)
        bot_response = check_booking_intent(user_message, context_memory)

        # 2. OpenAI GPT (FIRST for price calculations, comparisons, intelligent responses)
        # Skip FAQ for complex questions - let GPT handle them with context
        # BUT skip GPT for greetings - use dedicated greeting response
        if not bot_response and not is_short_greeting:
            user_lower = user_message.lower()
            # Use GPT for: prices, calculations, comparisons, complex questions with context
            use_gpt = any(
                [
                    "ile" in user_lower and ("kosztuje" in user_lower or "kosz" in user_lower),
                    "czym różni" in user_lower or "różnica" in user_lower,
                    "porównaj" in user_lower or "porówna" in user_lower,
                    "comfort" in user_lower or "premium" in user_lower or "express" in user_lower,
                    len(user_message.split()) > 8,  # Complex questions
                    context_memory.get("square_meters")
                    or context_memory.get("city"),  # Has context
                ]
            )

            if use_gpt:
                bot_response = self._get_gpt_response(
                    user_message,
                    conversation,
                    context_memory,
                    sentiment_analysis,
                    conversation.session_id,
                )

        # 3. Standard FAQ (for simple, factual questions without context)
        if not bot_response:
            bot_response = check_faq(user_message)

        # 4. Check if message is unclear - offer clarification (skip if greeting or has useful data)
        # Don't show confusion if user just provided name, city, sqm, etc.
        has_useful_data = any(
            [
                context_memory.get("name"),
                context_memory.get("city"),
                context_memory.get("square_meters"),
                context_memory.get("property_type"),
                context_memory.get("budget"),
            ]
        )

        if (
            not bot_response
            and len(user_message.split()) <= 3
            and not is_short_greeting
            and not has_useful_data
        ):
            clarification = proactive_suggestions.get_smart_clarification(
                user_message, context_memory
            )
            if clarification:
                clarification_msg = clarification.get("message", "")
                clarification_msg = clarification_msg.replace("**", "")
                return clarification_msg, None

        # 5. OpenAI GPT (fallback for everything else)
        if not bot_response:
            bot_response = self._get_gpt_response(
                user_message,
                conversation,
                context_memory,
                sentiment_analysis,
                conversation.session_id,
            )

        # 5. Learned FAQ (as fallback)
        if not bot_response:
            bot_response = check_learned_faq(user_message)

        # 6. Final fallback with clarification and targeted ask
        if not bot_response:
            # If we have useful data, acknowledge and ask for missing fields
            if has_useful_data:
                missing = self._get_missing_fields(context_memory)
                if missing:
                    # Build acknowledgment
                    ack_parts = []
                    if context_memory.get("name"):
                        ack_parts.append(f"Cześć {context_memory['name']}!")
                    if context_memory.get("property_type"):
                        ack_parts.append(f"Świetnie, {context_memory['property_type']}")
                    if context_memory.get("square_meters"):
                        ack_parts.append(f"{context_memory['square_meters']} m²")

                    acknowledgment = " ".join(ack_parts) if ack_parts else "Super!"
                    question = self._build_targeted_question(missing)
                    bot_response = f"{acknowledgment} {question}"
                else:
                    bot_response = "Świetnie! Mam już podstawowe informacje. Chcesz poznać nasze pakiety wykończeniowe?"
            else:
                # Try clarification only if not a greeting and no useful data
                if not is_short_greeting:
                    clarification = proactive_suggestions.get_smart_clarification(
                        user_message, context_memory
                    )
                    if clarification:
                        bot_response = clarification.get("message", "")

                if not bot_response:
                    missing = self._get_missing_fields(context_memory)
                    fallback_count = context_memory.get("fallback_count", 0) + 1
                    context_memory["fallback_count"] = fallback_count

                    if missing and fallback_count < 3:
                        bot_response = self._build_targeted_question(missing)
                    else:
                        bot_response = "Zbierzmy to szybko: podaj proszę miasto, typ (dom/mieszkanie), metraż i budżet (lub brak budżetu)."

        # Strip markdown bold if model returns it
        bot_response = bot_response.replace("**", "")

        # Add empathetic prefix based on sentiment
        if sentiment_analysis:
            empathy_prefix = sentiment_service.get_empathetic_response_prefix(
                sentiment_analysis.get("sentiment"), sentiment_analysis.get("score", 0)
            )
            if empathy_prefix:
                bot_response = empathy_prefix + bot_response

        # Generate follow-up question
        follow_up = generate_follow_up_question(
            context_memory, user_message, bot_response, conversation
        )

        return bot_response, follow_up

    def _get_missing_fields(self, context_memory: Dict) -> list:
        missing = []
        if not context_memory.get("city"):
            missing.append("city")
        if not context_memory.get("property_type"):
            missing.append("property_type")
        if not context_memory.get("square_meters"):
            missing.append("square_meters")
        if not context_memory.get("budget"):
            missing.append("budget")
        return missing

    def _build_targeted_question(self, missing: list) -> str:
        # Ask for the most important missing field first
        if "city" in missing:
            return "Podaj proszę miasto inwestycji."
        if "property_type" in missing:
            return "To dom czy mieszkanie?"
        if "square_meters" in missing:
            return "Ile metrów ma nieruchomość (podaj m2)?"
        if "budget" in missing:
            return "Jaki masz budżet (może być przybliżony lub brak budżetu)?"
        return "Podaj proszę miasto, typ (dom/mieszkanie), metraż i budżet (lub brak budżetu)."

    def _handle_escalation(
        self, sentiment_analysis: Dict, conversation: ChatConversation
    ) -> Tuple[str, Optional[str]]:
        """Handle escalation to human agent"""
        reason = sentiment_analysis.get("escalation_reason")

        # Mark conversation for human review
        conversation.needs_human_review = True  # Will add this column
        db.session.commit()

        escalation_messages = {
            "critical_frustration": "Rozumiem Twoją frustrację. Przekazuję sprawę do naszego doradcy, który skontaktuje się z Tobą w ciągu 15 minut. Czy mogę prosić o Twój numer telefonu?",
            "negative_streak": "Widzę, że masz wiele wątpliwości. Chętnie połączę Cię z naszym specjalistą, który odpowie na wszystkie pytania. Jak najlepiej się z Tobą skontaktować?",
        }

        message = escalation_messages.get(
            reason, "Przekazuję sprawę do naszego zespołu. Jak możemy się z Tobą skontaktować?"
        )

        return message, None

    @retry_openai_api
    def _get_gpt_response(
        self,
        user_message: str,
        conversation: ChatConversation,
        context_memory: Dict,
        sentiment_analysis: Dict = None,
        session_id: Optional[str] = None,
    ) -> Optional[str]:
        """Get response from configured LLM provider with retry logic"""

        from src.routes.chatbot import SYSTEM_PROMPT

        if not self._gpt_enabled:
            print("[GPT] GPT_FALLBACK_ENABLED=false – skipping GPT call")
            return None

        if session_id and not self._allow_gpt_call(session_id):
            print(
                f"[GPT] Rate limit reached for session {session_id} – skipping GPT call and using fallback."
            )
            return None

        history = (
            ChatMessage.query.filter_by(conversation_id=conversation.id)
            .order_by(ChatMessage.timestamp.asc())
            .all()
        )

        history_limit = 10
        history_dicts = [{"sender": m.sender, "message": m.message} for m in history]
        context = ""
        if len(history) > history_limit:
            older = history_dicts[:-history_limit]
            recent = history_dicts[-history_limit:]
            older_summary = summarization_service.generate_summary(context_memory, older)
            context = f"(Streszczenie wcześniejszych wiadomości: {older_summary})\n"
            history_dicts = recent

        context += "\n".join(
            [
                f"{'User' if msg['sender'] == 'user' else 'Bot'}: {msg['message']}"
                for msg in history_dicts
            ]
        )

        memory_prompt = self._build_memory_prompt(context_memory)

        print(f"[GPT] Processing: {user_message[:50]}...")
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT + memory_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nUser: {user_message}"},
        ]

        bot_response = run_llm(messages, temperature=0.7, max_tokens=500)
        if bot_response:
            print(f"[GPT] Response: {bot_response[:100]}...")
        return bot_response

    def _allow_gpt_call(self, session_id: str) -> bool:
        """Simple in-memory rate limit for GPT calls per session."""
        now = time.time()
        record = self._gpt_call_tracker.get(session_id, {"start": now, "count": 0})
        window_elapsed = now - record["start"]

        if window_elapsed > self._gpt_call_window_sec:
            record = {"start": now, "count": 0}

        if record["count"] >= self._gpt_calls_per_window:
            return False

        record["count"] += 1
        self._gpt_call_tracker[session_id] = record
        return True

    def _build_memory_prompt(self, context_memory: Dict) -> str:
        """Build comprehensive memory prompt for GPT"""
        from src.routes.chatbot import recommend_package

        memory_items = []

        if context_memory.get("name"):
            memory_items.append(f"📝 Imię: {context_memory['name']}")
        if context_memory.get("city"):
            memory_items.append(f"📍 Miasto: {context_memory['city']}")
        if context_memory.get("square_meters"):
            memory_items.append(f"📐 Metraż: {context_memory['square_meters']}m²")
        if context_memory.get("budget"):
            budget = context_memory["budget"]
            memory_items.append(f"💰 Budżet: ~{budget:,} zł")
            # Calculate budget per m² if we have both
            if context_memory.get("square_meters"):
                try:
                    sqm = int(context_memory["square_meters"])
                    per_sqm = int(budget / sqm)
                    memory_items.append(f"💵 Budżet/m²: ~{per_sqm:,} zł/m²")

                    # Get package recommendation
                    recommendation = recommend_package(budget, sqm)
                    if recommendation:
                        memory_items.append(f"⭐ REKOMENDACJA: {recommendation['reason']}")
                except Exception as e:
                    print(f"[Memory] Error calculating recommendation: {e}")
        if context_memory.get("package"):
            memory_items.append(f"📦 Zainteresowany pakiet: {context_memory['package']}")
        if context_memory.get("email"):
            memory_items.append(f"✉️ Email: {context_memory['email']}")
        if context_memory.get("phone"):
            memory_items.append(f"📞 Telefon: {context_memory['phone']}")

        if memory_items:
            return (
                "\n\n🧠 ZAPAMIĘTANY KONTEKST KLIENTA (UŻYJ W ODPOWIEDZI!):\n"
                + "\n".join(memory_items)
                + "\n\n⚠️ KRYTYCZNE: 1) Potwierdź te dane na początku odpowiedzi, 2) Przelicz ceny dla tego metrażu, 3) Użyj rekomendacji pakietu!"
            )
        return ""

    def _handle_confirmation(
        self, conversation: ChatConversation, context_memory: Dict
    ) -> Tuple[str, None]:
        """Handle user confirming data - create lead"""
        try:
            # Check if lead already exists
            from src.routes.chatbot import generate_conversation_summary, suggest_next_best_action

            existing_lead = Lead.query.filter_by(session_id=conversation.session_id).first()
            if existing_lead:
                return "Lead już został utworzony! 👍", None

            # Get all messages for ML scoring
            all_messages = (
                ChatMessage.query.filter_by(conversation_id=conversation.id)
                .order_by(ChatMessage.timestamp.asc())
                .all()
            )

            # Calculate lead score using ML (with rule-based fallback)
            lead_score = self._calculate_lead_score_ml(context_memory, conversation, all_messages)

            # Generate summary
            conv_summary = generate_conversation_summary(all_messages, context_memory)

            # Create lead
            lead = Lead(
                session_id=conversation.session_id,
                name=context_memory.get("name", "Unknown"),
                email=context_memory.get("email"),
                phone=context_memory.get("phone"),
                location=context_memory.get("city"),
                property_size=context_memory.get("square_meters"),
                interested_package=context_memory.get("package"),
                source="chatbot",
                status="qualified",
                lead_score=lead_score,
                conversation_summary=conv_summary,
                data_confirmed=True,
                last_interaction=datetime.now(timezone.utc),
            )

            # Save lead with retry logic
            from sqlalchemy.exc import OperationalError

            logger = logging.getLogger(__name__)
            max_retries = 2
            retry_count = 0

            while retry_count < max_retries:
                try:
                    db.session.add(lead)
                    db.session.flush()

                    # Suggest next action
                    next_action = suggest_next_best_action(context_memory, lead_score)
                    lead.notes = f"Next Action: {next_action}"

                    # Sync with Monday.com (with retry)
                    self._sync_with_monday(lead, context_memory, lead_score, next_action)

                    db.session.commit()
                    break  # Success
                except OperationalError as e:
                    retry_count += 1
                    db.session.rollback()
                    error_msg = str(e).lower()

                    if "server closed" in error_msg or "connection" in error_msg:
                        if retry_count < max_retries:
                            wait_time = 1 * retry_count
                            logger.warning(
                                f"⚠️ DB error saving lead (attempt {retry_count}/{max_retries}), "
                                f"retrying in {wait_time}s"
                            )
                            time.sleep(wait_time)
                            db.engine.dispose()
                        else:
                            logger.error(f"❌ Failed to save lead after {max_retries} attempts")
                            raise
                    else:
                        logger.error(f"❌ Non-retryable error saving lead: {str(e)[:150]}")
                        raise
                except Exception as e:
                    logger.error(f"❌ Unexpected error saving lead: {str(e)[:150]}")
                    db.session.rollback()
                    raise

            return (
                f"✅ Świetnie! Twoje dane zostały zapisane (Lead Score: {lead_score}/100). "
                f"Nasz zespół skontaktuje się z Tobą wkrótce!",
                None,
            )

        except Exception as e:
            print(f"[Lead Creation] Error: {e}")
            db.session.rollback()
            return "Przepraszam, wystąpił problem. Spróbuj ponownie później.", None

    @retry_monday_api
    def _sync_with_monday(
        self, lead: Lead, context_memory: Dict, lead_score: int, next_action: str
    ):
        """Sync lead with Monday.com with retry logic"""
        try:
            from src.integrations.monday_client import MondayClient
            from src.models.chatbot import CompetitiveIntel

            # Check for competitive mentions
            competitor_intel = (
                CompetitiveIntel.query.filter_by(session_id=lead.session_id)
                .order_by(CompetitiveIntel.created_at.desc())
                .first()
            )
            competitor_name = competitor_intel.competitor_name if competitor_intel else None

            monday = MondayClient()
            monday_item_id = monday.create_lead_item(
                {
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "message": f"Score: {lead_score}/100 | {lead.conversation_summary}",
                    "property_type": "Mieszkanie",
                    "budget": context_memory.get("square_meters", ""),
                    "lead_score": lead_score,
                    "competitor_mentioned": competitor_name,
                    "next_action": next_action,
                }
            )

            if monday_item_id:
                lead.monday_item_id = monday_item_id
                print(f"[Monday] Lead created: {monday_item_id}")
            else:
                raise Exception("Monday.com returned no item_id")

        except Exception as e:
            print(f"[Monday] Sync failed: {e}")
            # Add to failed operations queue
            failed_operations.add(
                "monday_lead",
                {
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "lead_score": lead_score,
                },
                str(e),
            )
            raise  # Re-raise for retry mechanism

    def _save_message(self, conversation_id: int, message: str, sender: str):
        """Save message to database with retry logic for connection failures"""
        import logging
        import time

        from sqlalchemy.exc import OperationalError

        logger = logging.getLogger(__name__)
        max_retries = 2
        retry_count = 0

        while retry_count < max_retries:
            try:
                msg = ChatMessage(
                    conversation_id=conversation_id,
                    message=message,
                    sender=sender,
                    timestamp=datetime.now(timezone.utc),
                )
                db.session.add(msg)
                db.session.flush()
                db.session.commit()  # Explicit commit
                return  # Success
            except OperationalError as e:
                retry_count += 1
                db.session.rollback()
                error_msg = str(e).lower()

                # Only retry on connection-level errors, not constraint violations
                if "server closed" in error_msg or "connection" in error_msg:
                    if retry_count < max_retries:
                        wait_time = 1 * retry_count  # 1s, then 2s
                        logger.warning(
                            f"⚠️ DB connection error (attempt {retry_count}/{max_retries}), "
                            f"retrying in {wait_time}s: {str(e)[:100]}"
                        )
                        time.sleep(wait_time)
                        # Force reconnect
                        try:
                            db.engine.dispose()
                        except Exception as dispose_err:
                            logger.warning(f"Failed to dispose connection: {dispose_err}")
                    else:
                        logger.error(
                            f"❌ Failed to save message after {max_retries} attempts: {str(e)[:150]}"
                        )
                        raise  # Re-raise after retries exhausted
                else:
                    # Non-connection error, don't retry
                    logger.error(f"❌ Non-retryable DB error: {str(e)[:150]}")
                    raise
            except Exception as e:
                # Other exceptions - don't retry
                logger.error(f"❌ Unexpected error saving message: {str(e)[:150]}")
                db.session.rollback()
                raise

    def _calculate_lead_score_ml(
        self, context_memory: Dict, conversation: ChatConversation, messages: list
    ) -> int:
        """
        Calculate lead score using ML model (with rule-based fallback)

        Args:
            context_memory: Context data
            conversation: ChatConversation object
            messages: List of ChatMessage objects

        Returns:
            Lead score (0-100)
        """
        try:
            from src.models.chatbot import CompetitiveIntel
            from src.services.lead_scoring_ml import lead_scorer_ml

            # Build conversation data for ML
            user_messages = [msg.message for msg in messages if msg.sender == "user"]
            timestamps = [msg.timestamp for msg in messages]

            duration = 0
            if len(timestamps) >= 2:
                duration = (timestamps[-1] - timestamps[0]).total_seconds() / 60.0

            # Check for competitive mention
            competitive_intel = CompetitiveIntel.query.filter_by(
                session_id=conversation.session_id
            ).first()

            # Check for booking intent
            has_booking = any("zencal" in msg.message.lower() for msg in messages)

            conversation_data = {
                "message_count": len(messages),
                "duration_minutes": duration,
                "messages": user_messages,
                "timestamps": timestamps,
                "has_competitive_mention": competitive_intel is not None,
                "has_booking_intent": has_booking,
            }

            # Use ML model to predict score
            score = lead_scorer_ml.predict_score(context_memory, conversation_data)

            print(f"[Lead Scoring] ML score: {score}/100")
            return score

        except Exception as e:
            print(f"[Lead Scoring] ML error, using rule-based fallback: {e}")
            # Fallback to rule-based scoring
            from src.routes.chatbot import calculate_lead_score

            return calculate_lead_score(context_memory, len(messages))

    def _try_create_lead(
        self, conversation: ChatConversation, context_memory: Dict, session_id: str
    ) -> Optional[Dict]:
        """
        Try to auto-create lead if enough data is available
        Returns: dict with lead info or None if no lead created
        """
        try:
            print(
                f"[Lead Creation] Checking... context: name={context_memory.get('name')}, email={context_memory.get('email')}, phone={context_memory.get('phone')}"
            )

            # Check if lead already exists
            existing_lead = Lead.query.filter_by(session_id=session_id).first()
            if existing_lead:
                print(f"[Lead Creation] Lead already exists: {existing_lead.id}")
                return None

            # Require name + (email OR phone)
            has_contact = context_memory.get("name") and (
                context_memory.get("email") or context_memory.get("phone")
            )
            if not has_contact:
                print("[Lead Creation] Insufficient data - skipping lead creation")
                return None

            print("[Lead Creation] Creating lead from conversation data...")

            # Calculate lead score
            messages = ChatMessage.query.filter_by(conversation_id=conversation.id).all()
            lead_score = self._calculate_lead_score_ml(context_memory, conversation, messages)

            # Generate conversation summary
            from src.routes.chatbot import generate_conversation_summary

            conv_summary = generate_conversation_summary(messages, context_memory)

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
                status="new",
                lead_score=lead_score,
                conversation_summary=conv_summary,
                data_confirmed=False,
                last_interaction=datetime.now(timezone.utc),
            )

            # Save lead with retry logic
            from sqlalchemy.exc import OperationalError

            logger = logging.getLogger(__name__)
            max_retries = 2
            retry_count = 0

            while retry_count < max_retries:
                try:
                    db.session.add(lead)
                    db.session.flush()
                    print(f"[Lead Creation] Lead created: {lead.id} (score: {lead_score})")
                    break  # Success
                except OperationalError as e:
                    retry_count += 1
                    db.session.rollback()
                    error_msg = str(e).lower()

                    if "server closed" in error_msg or "connection" in error_msg:
                        if retry_count < max_retries:
                            wait_time = 1 * retry_count
                            logger.warning(
                                f"⚠️ DB error creating lead (attempt {retry_count}/{max_retries}), "
                                f"retrying in {wait_time}s"
                            )
                            time.sleep(wait_time)
                            db.engine.dispose()
                        else:
                            logger.error(f"❌ Failed to create lead after {max_retries} attempts")
                            raise
                    else:
                        logger.error(f"❌ Non-retryable error creating lead: {str(e)[:150]}")
                        raise
                except Exception as e:
                    logger.error(f"❌ Unexpected error creating lead: {str(e)[:150]}")
                    db.session.rollback()
                    raise

            # Try to sync with Monday.com
            try:
                monday_api_key = os.getenv("MONDAY_API_KEY")
                if monday_api_key:
                    from src.integrations.monday_client import MondayClient
                    from src.routes.chatbot import suggest_next_best_action

                    next_action = suggest_next_best_action(context_memory, lead_score)

                    # Check for competitive mentions
                    competitor_intel = (
                        CompetitiveIntel.query.filter_by(session_id=session_id)
                        .order_by(CompetitiveIntel.created_at.desc())
                        .first()
                    )
                    competitor_name = competitor_intel.competitor_name if competitor_intel else None

                    monday_client = MondayClient(api_key=monday_api_key)
                    monday_item_id = monday_client.create_lead_item(
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
                        print(f"[Monday] Lead synced: {monday_item_id} (score: {lead_score})")

                        # Log high-priority leads
                        if lead_score >= 70:
                            print(
                                f"🔥 HIGH-PRIORITY LEAD from chatbot: {lead.name}, score: {lead_score}"
                            )
                    else:
                        print("[Monday] Failed to create lead item")

            except Exception as monday_error:
                print(f"[Monday Sync] Error: {monday_error}")
                # Don't fail lead creation if Monday sync fails

            db.session.commit()

            return {
                "lead_id": lead.id,
                "lead_score": lead_score,
                "monday_item_id": lead.monday_item_id,
            }

        except Exception as e:
            print(f"[Lead Creation] Error: {e}")
            db.session.rollback()
            return None

    def get_gpt_stats(self, session_id: str = None) -> Dict[str, int]:
        """
        Get GPT call statistics, optionally for a specific session

        Args:
            session_id: If provided, returns per-session stats. Otherwise returns aggregate.

        Returns:
            Dict with keys: total_calls, success_calls, drops, rate_limit_drops,
                           placeholder_key_drops, drop_rate_percent
        """
        if session_id and session_id in self._gpt_call_tracker:
            # Per-session stats (calls only, no drop tracking per session currently)
            session_data = self._gpt_call_tracker[session_id]
            call_times = session_data.get("calls", [])
            return {
                "session_id": session_id,
                "calls_in_window": len(call_times),
                "window_seconds": self._gpt_call_window_sec,
                "limit": self._gpt_calls_per_window,
                "remaining": max(0, self._gpt_calls_per_window - len(call_times)),
            }
        else:
            # Aggregate stats
            total = self._gpt_success_count + self._gpt_drop_count
            drop_rate = round((self._gpt_drop_count / total * 100), 2) if total > 0 else 0.0
            return {
                "total_calls": total,
                "success_calls": self._gpt_success_count,
                "drops": self._gpt_drop_count,
                "rate_limit_drops": self._gpt_rate_limit_drops,
                "placeholder_key_drops": self._gpt_placeholder_key_drops,
                "drop_rate_percent": drop_rate,
            }

    def log_gpt_success(self, session_id: str):
        """Log successful GPT call"""
        self._gpt_success_count += 1
        # Also track in per-session limiter
        now = time.time()
        if session_id not in self._gpt_call_tracker:
            self._gpt_call_tracker[session_id] = {"calls": []}
        self._gpt_call_tracker[session_id]["calls"].append(now)
        # Clean old calls
        cutoff = now - self._gpt_call_window_sec
        self._gpt_call_tracker[session_id]["calls"] = [
            t for t in self._gpt_call_tracker[session_id]["calls"] if t > cutoff
        ]

    def log_gpt_drop(self, session_id: str, reason: str):
        """
        Log dropped GPT call with reason

        Args:
            session_id: Session identifier
            reason: One of 'rate_limit', 'placeholder_key', 'other'
        """
        self._gpt_drop_count += 1
        if reason == "rate_limit":
            self._gpt_rate_limit_drops += 1
            print(
                f"[GPT Drop] Rate limit exceeded for {session_id} ({self._gpt_rate_limit_drops} total)"
            )
        elif reason == "placeholder_key":
            self._gpt_placeholder_key_drops += 1
            print(
                f"[GPT Drop] Placeholder key detected for {session_id} ({self._gpt_placeholder_key_drops} total)"
            )
        else:
            print(f"[GPT Drop] {reason} for {session_id}")

    def _restore_returning_customer_context(
        self, session_id: str, context_memory: Dict
    ) -> Optional[Dict]:
        """
        PERSISTENT MEMORY: Restore context from previous conversations

        Checks if user is a returning customer (has previous leads) and loads their context:
        - Name, email, phone
        - Previous package interests
        - Previous property details (size, type, location)
        - Conversation history context

        Args:
            session_id: Current session ID
            context_memory: Current conversation context to restore into

        Returns:
            Dict with restored customer context or None if not a returning customer
        """
        try:
            from src.models.chatbot import Lead

            # Strategy: Look for leads by email OR phone (most reliable identifiers)
            # If found in current session_id, don't count as "returning"
            # If found in different session_id, it's a returning customer
            # First check: Do we already have identifying info?
            existing_email = context_memory.get("email")
            existing_phone = context_memory.get("phone")

            previous_leads = []

            # PRIVACY & SECURITY: Only restore context if user has provided email or phone
            # Without explicit identifier, user gets fresh start (prevents data leakage to wrong user)
            
            # Case 1: User has email - find by email
            if existing_email:
                previous_leads = (
                    Lead.query.filter_by(email=existing_email)
                    .filter(Lead.session_id != session_id)
                    .all()
                )

            # Case 2: No email yet, but find by phone
            elif existing_phone:
                previous_leads = (
                    Lead.query.filter_by(phone=existing_phone)
                    .filter(Lead.session_id != session_id)
                    .all()
                )
            else:
                # No email or phone provided - don't restore data from other sessions
                # User gets fresh start unless they explicitly identify themselves
                return None

            if not previous_leads:
                return None

            # Found returning customer! Restore their context
            latest_lead = max(previous_leads, key=lambda lead: lead.created_at)

            # Restore previous context (but don't overwrite current session data)
            restored_context = {
                "name": latest_lead.name or context_memory.get("name"),
                "email": latest_lead.email or context_memory.get("email"),
                "phone": latest_lead.phone or context_memory.get("phone"),
                "location": latest_lead.location or context_memory.get("location"),
                "property_type": latest_lead.property_type or context_memory.get("property_type"),
                "square_meters": latest_lead.property_size or context_memory.get("square_meters"),
                "previous_package_interest": latest_lead.interested_package,
                "previous_interaction": (
                    latest_lead.last_interaction.isoformat()
                    if latest_lead.last_interaction
                    else None
                ),
                "previous_lead_score": latest_lead.lead_score,
            }

            # Update context_memory with restored data
            context_memory.update(restored_context)

            print(f"[PersistentMemory] Restored context for {restored_context.get('name')}")
            return restored_context

        except Exception as e:
            print(f"[PersistentMemory] Error restoring customer context: {str(e)}")
            return None

    def export_aggregate_metrics(self) -> str:
        """
        Export aggregate GPT metrics as JSON string for monitoring/dashboard

        Returns:
            JSON string with all metrics
        """
        import json

        metrics = self.get_gpt_stats()
        metrics["timestamp"] = datetime.now(timezone.utc).isoformat()
        metrics["gpt_enabled"] = self._gpt_enabled
        metrics["config"] = {
            "calls_per_window": self._gpt_calls_per_window,
            "window_seconds": self._gpt_call_window_sec,
        }
        return json.dumps(metrics, indent=2)


# Global instance
message_handler = MessageHandler()
