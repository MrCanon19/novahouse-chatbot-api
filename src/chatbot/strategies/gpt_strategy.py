"""
GPT Strategy - Uses OpenAI GPT to generate responses when FAQ doesn't match
"""
import json
import logging
import os
from typing import Any, Dict, Optional

from openai import OpenAI
from sqlalchemy.orm import Session

from src.config.prompts import SYSTEM_PROMPT
from src.models.chatbot import ChatMessage
from src.utils.polish_declension import PolishDeclension

from .base import ChatStrategy

# Configuration: Message history limit (shorter = szybsze odpowiedzi)
MESSAGE_HISTORY_LIMIT = int(os.getenv("MESSAGE_HISTORY_LIMIT", "15"))


class GptStrategy(ChatStrategy):
    """
    Strategy that uses OpenAI GPT to generate responses when no FAQ match is found.
    This is the fallback strategy that should run after FAQ checks.
    """

    def __init__(self, openai_client: Optional[OpenAI], gpt_model: str, db_session: Session):
        """
        Initialize GPT strategy.

        Args:
            openai_client: OpenAI client instance (can be None if not configured)
            gpt_model: Model name to use (e.g., "gpt-4o-mini", "gpt-4o")
            db_session: Database session for querying conversation history
        """
        self.openai_client = openai_client
        self.gpt_model = gpt_model
        self.db_session = db_session

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes the context and generates a GPT response if no bot_response exists yet.

        Args:
            context: The current chat context. Must contain:
                - 'user_message': The user's message
                - 'conversation': ChatConversation object
                - 'context_memory': Dict with extracted context (name, city, etc.)
                - 'bot_response': Optional, if already set by previous strategy, skip GPT

        Returns:
            Updated context with 'bot_response' set if GPT was used.
        """
        # Skip if bot_response already exists (from FAQ or other strategy)
        if context.get("bot_response"):
            return context

        # Skip if OpenAI client is not available
        if not self.openai_client:
            logging.warning("[GPT Strategy] OpenAI client not available - skipping")
            return context

        user_message = context.get("user_message")
        conversation = context.get("conversation")
        context_memory = context.get("context_memory", {})

        if not user_message or not conversation:
            return context

        try:
            # Get conversation history (configurable limit, default 20)
            history = (
                self.db_session.query(ChatMessage)
                .filter_by(conversation_id=conversation.id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(MESSAGE_HISTORY_LIMIT)
                .all()
            )

            # Build context string from history
            history_context = "\n".join(
                [
                    f"{'User' if msg.sender == 'user' else 'Bot'}: {msg.message}"
                    for msg in reversed(history[:-1])  # Exclude current message
                ]
            )

            # Filter input before sending to LLM
            from src.services.llm.input_filter import LLMInputFilter
            from src.services.monitoring import MetricsService

            filtered_message, is_safe, reason = LLMInputFilter.filter_input(user_message)
            
            if not is_safe:
                print(f"[GPT Strategy] Input blocked: {reason}")
                MetricsService.increment_llm_input_blocked()
                context["bot_response"] = LLMInputFilter.get_safe_response()
                return context

            # Build memory prompt with proper name declension
            memory_prompt = self._build_memory_prompt(context_memory)

            # Prepare messages for OpenAI
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT + memory_prompt},
                {
                    "role": "user",
                    "content": f"Context:\n{history_context}\n\nUser: {filtered_message}",
                },
            ]

            print(f"[GPT Strategy] Processing: {filtered_message[:50]}...")

            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model=self.gpt_model,
                messages=messages,
                max_tokens=250,
                temperature=0.7,
            )

            bot_response = response.choices[0].message.content

            # Filter output before sending to user
            if bot_response:
                from src.services.llm.output_filter import LLMOutputFilter
                from src.services.monitoring import MetricsService
                
                filtered_response, output_safe, output_reason = LLMOutputFilter.filter_output(
                    bot_response, context_memory
                )
                
                if output_safe:
                    context["bot_response"] = filtered_response
                    print(f"[GPT Strategy] Response: {filtered_response[:100]}...")
                else:
                    print(f"[GPT Strategy] Output blocked: {output_reason}")
                    MetricsService.increment_llm_output_blocked()
                    context["bot_response"] = LLMOutputFilter.get_safe_fallback()
            else:
                print("[GPT Strategy] Empty response from GPT")
                context["bot_response"] = "Przepraszam, nie udało mi się wygenerować odpowiedzi. Spróbuj ponownie."

        except Exception as e:
            from src.services.monitoring import MetricsService, capture_exception
            
            print(f"[GPT Strategy ERROR] {type(e).__name__}: {e}")
            MetricsService.increment_llm_error()
            capture_exception(e, extra={"user_message": user_message[:100]})
            
            # Fallback response on error
            context["bot_response"] = (
                "Przepraszam, wystąpił błąd podczas przetwarzania Twojej wiadomości. "
                "Spróbuj ponownie lub skontaktuj się z nami bezpośrednio."
            )

        return context

    def _build_memory_prompt(self, context_memory: Dict[str, Any]) -> str:
        """
        Build memory prompt with proper name declension for GPT.

        Args:
            context_memory: Dictionary with extracted context (name, city, etc.)

        Returns:
            Formatted string with memory information
        """
        if not context_memory:
            return ""

        memory_items = []

        # Name with declension
        if context_memory.get("name"):
            name = context_memory["name"]
            declined_name = PolishDeclension.decline_full_name(name)
            is_polish = PolishDeclension.is_polish_name(name.split()[0] if name else "")

            memory_items.append(
                f"Imię: {name} (wołacz: {declined_name}, polskie: {is_polish})"
            )

        # City
        if context_memory.get("city"):
            memory_items.append(f"Miasto: {context_memory['city']}")

        # Square meters
        if context_memory.get("square_meters"):
            memory_items.append(f"Metraż: {context_memory['square_meters']}m²")

        # Package
        if context_memory.get("package"):
            memory_items.append(f"Interesujący pakiet: {context_memory['package']}")

        # Email
        if context_memory.get("email"):
            memory_items.append(f"Email: {context_memory['email']}")

        # Phone
        if context_memory.get("phone"):
            memory_items.append(f"Telefon: {context_memory['phone']}")

        # Budget
        if context_memory.get("budget"):
            memory_items.append(f"Budżet: {context_memory['budget']} zł")

        if memory_items:
            return "\n\nZapamiętane info o kliencie:\n" + "\n".join(memory_items)

        return ""

