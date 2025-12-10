import json
from datetime import datetime, timezone
from typing import Any, Dict

from sqlalchemy.orm import Session

from src.models.chatbot import ChatConversation, ChatMessage

from .base import ChatStrategy


class PersistenceStrategy(ChatStrategy):
    """
    A strategy to persist the chat messages and conversation context to the database.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Saves the user message, bot response, and updated conversation context
        to the database.

        Args:
            context: The current chat context, containing 'user_message',
                     'bot_response', 'conversation', and 'context_memory'.

        Returns:
            The updated context (primarily for consistency, no major changes expected).
        """
        user_message = context.get("user_message")
        bot_response = context.get("bot_response")
        conversation: ChatConversation = context.get("conversation")
        context_memory = context.get("context_memory", {})

        if not conversation:
            print("[ERROR] PersistenceStrategy received context without a conversation object.")
            return context

        try:
            # Save user message
            user_msg = ChatMessage(
                conversation_id=conversation.id,
                message=user_message,
                sender="user",
                timestamp=datetime.now(timezone.utc),
            )
            self.db_session.add(user_msg)

            # Save bot response
            if bot_response:
                bot_msg = ChatMessage(
                    conversation_id=conversation.id,
                    message=bot_response,
                    sender="bot",
                    timestamp=datetime.now(timezone.utc),
                )
                self.db_session.add(bot_msg)

            # Update conversation context
            conversation.context_data = json.dumps(context_memory)
            self.db_session.add(conversation)  # Mark as modified

            # Commit all changes
            self.db_session.commit()
            print(f"Messages and context for conversation {conversation.id} persisted.")

        except Exception as e:
            self.db_session.rollback()
            print(f"[ERROR] PersistenceStrategy failed to save data: {e}")
            # Depending on requirements, could set an error in context or re-raise
            # For now, just log and rollback, allowing the chat flow to potentially continue.

        return context
