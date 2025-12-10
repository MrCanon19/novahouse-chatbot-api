import json
from datetime import datetime, timezone
from typing import Any, Dict

from sqlalchemy.orm import Session

from src.models.chatbot import ChatConversation

from .base import ChatStrategy


class ConversationInitializationStrategy(ChatStrategy):
    """
    A strategy to initialize or load a chat conversation and its context memory.
    This should be the first strategy in the pipeline.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Finds an existing ChatConversation based on session_id or creates a new one.
        Loads the conversation's context_data into context_memory.

        Args:
            context: The current chat context. Must contain 'session_id'.

        Returns:
            The updated context with 'conversation' (ChatConversation object)
            and 'context_memory' (dict) added.
        """
        session_id = context.get("session_id")

        if not session_id:
            raise ValueError(
                "session_id must be provided in the context for ConversationInitializationStrategy."
            )

        conversation = (
            self.db_session.query(ChatConversation).filter_by(session_id=session_id).first()
        )

        if not conversation:
            conversation = ChatConversation(
                session_id=session_id,
                started_at=datetime.now(timezone.utc),
                context_data=json.dumps({}),  # Initialize empty context
            )
            self.db_session.add(conversation)
            self.db_session.flush()  # Flush to get conversation.id if new

        # Load context_data (JSON string) into context_memory (dict)
        context_memory = json.loads(conversation.context_data or "{}")

        context["conversation"] = conversation
        context["context_memory"] = context_memory

        return context
