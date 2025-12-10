from typing import Any, Dict

from src.services.extract_context_safe import extract_context_safe

from .base import ChatStrategy


class ContextExtractionStrategy(ChatStrategy):
    """
    A strategy to extract information (name, city, etc.) from the user message
    and update the conversation's context memory.
    """

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Uses the regex-based `extract_context_safe` service to parse the
        user's message and update the context_memory.

        Args:
            context: The current chat context. Must contain 'user_message'
                     and 'context_memory'.

        Returns:
            The updated context with potentially more data in 'context_memory'.
        """
        user_message = context.get("user_message")
        context_memory = context.get("context_memory", {})

        if not user_message:
            # Nothing to process
            return context

        # The core logic is still in the old service, but now it's wrapped
        # in our new strategy pattern.
        updated_memory = extract_context_safe(user_message, context_memory)

        context["context_memory"] = updated_memory

        return context
