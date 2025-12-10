from abc import ABC, abstractmethod
from typing import Any, Dict


class ChatStrategy(ABC):
    """
    Abstract base class for a chat processing strategy.
    """

    @abstractmethod
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes the chat context and returns an updated context.

        Each strategy takes the context, performs an action (like calling an API,
        checking a FAQ, or extracting information), and updates the context
        with new information (e.g., a bot response, extracted user data).

        Args:
            context: A dictionary containing all information about the current
                     chat state, including user message, session_id,
                     conversation history, etc.

        Returns:
            An updated context dictionary.
        """
