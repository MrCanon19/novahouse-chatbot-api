"""
Conversation State Machine
Manages chatbot conversation flow through defined states
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional, Tuple


class ConversationState(Enum):
    """Conversation states"""

    GREETING = "greeting"  # Initial greeting, no data yet
    COLLECTING_INFO = "collecting_info"  # Gathering: package, sqm, city
    QUALIFYING = "qualifying"  # Has interest, collecting contact info
    CONFIRMING = "confirming"  # Awaiting data confirmation
    CLOSED = "closed"  # Lead created or conversation abandoned


class StateTransition:
    """Valid state transitions"""

    TRANSITIONS = {
        ConversationState.GREETING: [ConversationState.COLLECTING_INFO, ConversationState.CLOSED],
        ConversationState.COLLECTING_INFO: [
            ConversationState.QUALIFYING,
            ConversationState.GREETING,
            ConversationState.CLOSED,
        ],
        ConversationState.QUALIFYING: [
            ConversationState.CONFIRMING,
            ConversationState.COLLECTING_INFO,
            ConversationState.CLOSED,
        ],
        ConversationState.CONFIRMING: [
            ConversationState.CLOSED,
            ConversationState.QUALIFYING,
        ],
        ConversationState.CLOSED: [],  # Terminal state
    }


class ConversationStateMachine:
    """
    State machine for managing conversation flow
    Ensures clean transitions and proper data collection
    """

    def __init__(self, initial_state: ConversationState = ConversationState.GREETING):
        self.current_state = initial_state
        self.state_history = [(initial_state, datetime.now(timezone.utc))]

    def can_transition(self, new_state: ConversationState) -> bool:
        """Check if transition is valid"""
        allowed = StateTransition.TRANSITIONS.get(self.current_state, [])
        return new_state in allowed

    def transition(self, new_state: ConversationState) -> Tuple[bool, Optional[str]]:
        """
        Attempt state transition

        Returns:
            (success: bool, error_message: Optional[str])
        """
        if not self.can_transition(new_state):
            return False, f"Invalid transition: {self.current_state.value} → {new_state.value}"

        self.current_state = new_state
        self.state_history.append((new_state, datetime.now(timezone.utc)))
        return True, None

    def determine_state(self, context_memory: Dict) -> ConversationState:
        """
        Determine appropriate state based on context memory

        Rules:
        - GREETING: No data collected
        - COLLECTING_INFO: Has some interest (package/sqm/city) but incomplete
        - QUALIFYING: Has interest + collecting contact info
        - CONFIRMING: Has all required data, awaiting confirmation
        - CLOSED: Lead created or abandoned
        """
        has_package = bool(context_memory.get("package"))
        has_sqm = bool(context_memory.get("square_meters"))
        has_city = bool(context_memory.get("city"))
        has_name = bool(context_memory.get("name"))
        has_contact = bool(context_memory.get("email") or context_memory.get("phone"))

        # No data at all
        if not any([has_package, has_sqm, has_city, has_name, has_contact]):
            return ConversationState.GREETING

        # Has interest but no contact
        has_interest = has_package or has_sqm
        if has_interest and not has_contact:
            return ConversationState.COLLECTING_INFO

        # Has interest + has name but missing contact details
        if has_interest and has_name and not has_contact:
            return ConversationState.QUALIFYING

        # Has complete data, ready to confirm
        if has_interest and has_name and has_contact:
            return ConversationState.CONFIRMING

        # Default to collecting info
        return ConversationState.COLLECTING_INFO

    def should_ask_confirmation(self, context_memory: Dict) -> bool:
        """Check if we should ask user to confirm data"""
        optional = ["email", "phone", "city", "square_meters", "package"]

        # Must have at least name
        if not context_memory.get("name"):
            return False

        # Must have at least one contact method
        has_contact = context_memory.get("email") or context_memory.get("phone")
        if not has_contact:
            return False

        # Should have at least 2 optional fields
        optional_count = sum(1 for field in optional if context_memory.get(field))
        return optional_count >= 2

    def get_next_required_field(self, context_memory: Dict) -> Optional[str]:
        """
        Determine next required field to collect

        Priority:
        1. package (interest signal)
        2. square_meters (for quote)
        3. city (for availability)
        4. name (for personalization)
        5. email/phone (for contact)
        """
        if not context_memory.get("package"):
            return "package"
        if not context_memory.get("square_meters"):
            return "square_meters"
        if not context_memory.get("city"):
            return "city"
        if not context_memory.get("name"):
            return "name"
        if not (context_memory.get("email") or context_memory.get("phone")):
            return "contact"
        return None

    def get_state_summary(self) -> Dict:
        """Get state machine summary for debugging"""
        return {
            "current_state": self.current_state.value,
            "state_count": len(self.state_history),
            "state_history": [
                {"state": state.value, "timestamp": ts.isoformat()}
                for state, ts in self.state_history
            ],
        }
