from typing import Any, Dict, List

from src.chatbot.strategies.base import ChatStrategy


class ChatPipeline:
    """
    Orchestrates the execution of multiple ChatStrategy instances in a defined order.
    """

    def __init__(self, strategies: List[ChatStrategy]):
        self.strategies = strategies

    def process(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes each strategy in the pipeline, passing the context from one
        to the next.

        Args:
            initial_context: The starting context for the chat processing.

        Returns:
            The final context after all strategies have been executed.
        """
        current_context = (
            initial_context.copy()
        )  # Start with a copy to avoid modifying external dict

        for strategy in self.strategies:
            current_context = strategy.process(current_context)
            # If a strategy sets a bot_response, and it's not meant to be overridden,
            # subsequent strategies might skip their processing or append to it.
            # The current design allows strategies to decide based on context content.

        return current_context
