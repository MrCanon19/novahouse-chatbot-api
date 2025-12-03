"""
Refactored Message Handler
Modular, clean, with state machine and validation
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

from src.models.chatbot import ChatConversation, ChatMessage, Lead, db
from src.services.context_validator import ContextValidator
from src.services.conversation_state_machine import ConversationStateMachine
from src.services.multi_turn_dialog import multi_turn_dialog
from src.services.proactive_suggestions import proactive_suggestions
from src.services.rate_limiter import conversation_limiter
from src.services.retry_handler import failed_operations, retry_monday_api, retry_openai_api
from src.services.sentiment_service import sentiment_service
from src.services.session_timeout import session_timeout_service
from src.services.summarization_service import summarization_service


class MessageHandler:
    """Handles chat message processing with state management"""

    def __init__(self):
        self.validator = ContextValidator()

    def process_message(self, user_message: str, session_id: str) -> Dict:
        """
        Main entry point for message processing

        Returns:
            dict with response, session_id, conversation_id, state
        """
        try:
            # 1. Rate limiting & spam detection
            spam_check = self._check_spam(session_id, user_message)
            if spam_check:
                return {"error": spam_check, "response": "Proszę zwolnić tempo wiadomości."}

            # 2. Find or create conversation
            conversation = self._get_or_create_conversation(session_id)

            # 3. Update session activity (for timeout detection)
            session_timeout_service.update_activity(session_id)

            # 4. Load and validate context
            context_memory = json.loads(conversation.context_data or "{}")

            # 5. Get message history for multi-turn dialog
            messages = ChatMessage.query.filter_by(conversation_id=conversation.id).all()
            message_history = [{"sender": m.sender, "message": m.message} for m in messages]

            # 6. Resolve references in multi-turn dialog (a srebrnego?, a w warszawie?)
            resolved_message = multi_turn_dialog.resolve_references(
                user_message, context_memory, message_history, session_id
            )
            if resolved_message != user_message:
                print(f"[MultiTurn] Resolved '{user_message}' -> '{resolved_message}'")
                user_message = resolved_message

            # 7. Initialize state machine
            state_machine = ConversationStateMachine()
            current_state = state_machine.determine_state(context_memory)
            state_machine.current_state = current_state

            # 8. Extract context from message
            context_memory = self._extract_and_validate_context(user_message, context_memory)

            # 9. Analyze sentiment in real-time
            sentiment_analysis = sentiment_service.analyze_message_sentiment(
                user_message, session_id
            )

            # Save user message
            self._save_message(conversation.id, user_message, "user")

            # 10. Generate response based on state
            bot_response, follow_up = self._generate_response(
                user_message, context_memory, conversation, state_machine, sentiment_analysis
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
            messages = ChatMessage.query.filter_by(conversation_id=conversation.id).all()
            message_history = [{"sender": m.sender, "message": m.message} for m in messages]

            # Calculate conversation duration
            duration_seconds = 0
            if conversation.started_at and messages:
                from datetime import timezone

                latest_message_time = max(m.timestamp for m in messages)
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
            conversation.conversation_summary = conversation_summary  # Will add this column
            db.session.commit()

            return {
                "response": bot_response + (f"\n\n{follow_up}" if follow_up else ""),
                "session_id": session_id,
                "conversation_id": conversation.id,
                "state": state_machine.current_state.value,
                "sentiment": sentiment_analysis,
                "suggestions": suggestions,
                "typing_indicator": True,  # Signal to frontend
                "summary": summarization_service.generate_short_summary(context_memory),
            }

        except Exception as e:
            print(f"[MessageHandler] Error: {e}")
            db.session.rollback()
            try:
                from src.utils.telegram_alert import send_telegram_alert

                send_telegram_alert(f"Błąd produkcyjny: {str(e)}")
            except Exception as alert_exc:
                print(f"[Telegram Alert] Failed: {alert_exc}")
            return {
                "error": str(e),
                "response": "Przepraszam, wystąpił problem. Spróbuj ponownie.",
            }

    def _check_spam(self, session_id: str, message: str) -> Optional[str]:
        """Check for spam patterns"""
        conversation_limiter.add_message(session_id, message)
        is_spam, reason = conversation_limiter.is_spam(session_id, message)
        if is_spam:
            print(f"[Spam] Detected for {session_id}: {reason}")
            return f"Spam detected: {reason}"
        return None

    def _get_or_create_conversation(self, session_id: str) -> ChatConversation:
        """Find or create conversation"""
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            conversation = ChatConversation(
                session_id=session_id,
                started_at=datetime.now(timezone.utc),
                context_data=json.dumps({}),
            )
            db.session.add(conversation)
            db.session.flush()
        return conversation

    def _extract_and_validate_context(self, message: str, existing_context: Dict) -> Dict:
        """Extract context from message and validate"""
        from src.routes.chatbot import extract_context

        # Extract context
        updated_context = extract_context(message, existing_context)

        # Validate and sanitize
        is_valid, sanitized, errors = self.validator.validate_context(updated_context)

        if errors:
            print(f"[Validation] Errors: {errors}")
            # Keep original values if validation failed
            for field, error in errors.items():
                if field in updated_context and field in existing_context:
                    updated_context[field] = existing_context[field]

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
            get_default_response,
        )

        # Check for data confirmation
        confirmation_intent = check_data_confirmation_intent(user_message)
        if confirmation_intent == "confirm" and conversation.awaiting_confirmation:
            return self._handle_confirmation(conversation, context_memory)

        # Check for escalation due to negative sentiment
        if sentiment_analysis and sentiment_analysis.get("should_escalate"):
            return self._handle_escalation(sentiment_analysis, conversation)

        # Response hierarchy (NEW ORDER - GPT earlier)
        bot_response = None

        # 1. Booking intent (highest priority)
        bot_response = check_booking_intent(user_message, context_memory)

        # 2. Standard FAQ (fast, no API call)
        if not bot_response:
            bot_response = check_faq(user_message)

        # 3. Check if message is unclear - offer clarification
        if not bot_response and len(user_message.split()) <= 3:
            clarification = proactive_suggestions.get_smart_clarification(
                user_message, context_memory
            )
            if clarification:
                return clarification.get("message", ""), None

        # 4. OpenAI GPT (early in hierarchy for better responses)
        if not bot_response:
            bot_response = self._get_gpt_response(
                user_message, conversation, context_memory, sentiment_analysis
            )

        # 5. Learned FAQ (as fallback)
        if not bot_response:
            bot_response = check_learned_faq(user_message)

        # 6. Final fallback with clarification
        if not bot_response:
            clarification = proactive_suggestions.get_smart_clarification(
                user_message, context_memory
            )
            if clarification:
                return clarification.get("message", ""), None
            bot_response = get_default_response(user_message)

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
    ) -> Optional[str]:
        """Get response from OpenAI GPT with retry logic"""
        try:
            from openai import OpenAI

            from src.routes.chatbot import SYSTEM_PROMPT

            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                print(
                    "ALERT: OPENAI_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
                )
            openai_client = OpenAI(api_key=openai_api_key)

            # Get conversation history
            history = (
                ChatMessage.query.filter_by(conversation_id=conversation.id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(10)
                .all()
            )

            context = "\n".join(
                [
                    f"{'User' if msg.sender == 'user' else 'Bot'}: {msg.message}"
                    for msg in reversed(history[:-1])
                ]
            )

            # Add memory context
            memory_prompt = self._build_memory_prompt(context_memory)

            print(f"[GPT] Processing: {user_message[:50]}...")
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT + memory_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nUser: {user_message}"},
            ]

            response = openai_client.chat.completions.create(
                model="gpt-4o-mini", messages=messages, max_tokens=500, temperature=0.7
            )

            bot_response = response.choices[0].message.content
            print(f"[GPT] Response: {bot_response[:100]}...")
            return bot_response

        except Exception as e:
            print(f"[GPT] Error: {e}")
            return None

    def _build_memory_prompt(self, context_memory: Dict) -> str:
        """Build memory prompt for GPT"""
        memory_items = []
        if context_memory.get("name"):
            memory_items.append(f"Imię: {context_memory['name']}")
        if context_memory.get("city"):
            memory_items.append(f"Miasto: {context_memory['city']}")
        if context_memory.get("square_meters"):
            memory_items.append(f"Metraż: {context_memory['square_meters']}m²")
        if context_memory.get("package"):
            memory_items.append(f"Pakiet: {context_memory['package']}")

        if memory_items:
            return "\n\nZapamiętane info o kliencie:\n" + "\n".join(memory_items)
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

            db.session.add(lead)
            db.session.flush()

            # Suggest next action
            next_action = suggest_next_best_action(context_memory, lead_score)
            lead.notes = f"Next Action: {next_action}"

            # Sync with Monday.com (with retry)
            self._sync_with_monday(lead, context_memory, lead_score, next_action)

            db.session.commit()

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
        """Save message to database"""
        msg = ChatMessage(
            conversation_id=conversation_id,
            message=message,
            sender=sender,
            timestamp=datetime.now(timezone.utc),
        )
        db.session.add(msg)
        db.session.flush()

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


# Global instance
message_handler = MessageHandler()
