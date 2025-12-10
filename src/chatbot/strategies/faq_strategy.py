from typing import Any, Dict

from src.services.faq_service import FaqService

from .base import ChatStrategy


class FaqStrategy(ChatStrategy):
    """
    A strategy to check if the user's message matches any known FAQs (learned or static).
    If a match is found, the bot_response is set in the context.
    """

    def __init__(self, faq_service: FaqService):
        self.faq_service = faq_service

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks for learned FAQs first, then static FAQs. If a response is found,
        it updates the context with the bot's response.

        Args:
            context: The current chat context, containing 'user_message'.

        Returns:
            The updated context, potentially with 'bot_response' set.
        """
        user_message = context.get("user_message")
        bot_response = None

        if not user_message:
            return context

        # 1. Check learned FAQs (higher priority)
        bot_response = self.faq_service.check_learned_faq(user_message)

        # 2. If no learned FAQ, check static FAQs
        if not bot_response:
            # Detect if the current message is an introduction (to prioritize GPT routing later)
            # This logic is copied from the old chatbot.py and should eventually be moved
            # to a more appropriate strategy or an intent detection module.
            intro_keywords = ["jestem", "nazywam się", "mam na imię", "to ja", "cześć jestem"]
            is_introduction = any(k in user_message.lower() for k in intro_keywords)

            # Skip static FAQ if this is an introduction
            if not is_introduction:
                bot_response = self.faq_service.check_faq(user_message)

        if bot_response:
            context["bot_response"] = bot_response

        return context
