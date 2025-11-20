"""
Multi-turn Dialog Service
Handles context references and anaphora resolution (a co z tym?, a w warszawie?)
"""

import re
from typing import Dict, List, Optional


class MultiTurnDialogService:
    """Resolves references in multi-turn conversations"""

    def __init__(self):
        self.session_context = {}  # Track what was discussed per session

    def resolve_references(
        self,
        current_message: str,
        context_memory: Dict,
        message_history: List[Dict],
        session_id: str,
    ) -> str:
        """
        Resolve references like 'a srebrnego?', 'a w warszawie?', 'a tamto?'

        Returns:
            Expanded message with resolved references
        """
        message_lower = current_message.lower().strip()

        # Pattern: "a X?" or "a co z X?"
        reference_patterns = [
            r"^a\s+(.+)\?*$",  # "a srebrnego?"
            r"^a\s+co\s+z\s+(.+)\?*$",  # "a co z tamtym?"
            r"^co\s+z\s+(.+)\?*$",  # "co z pakietem?"
            r"^jak\s+z\s+(.+)\?*$",  # "jak z ceną?"
            r"^(.+)\s+też\?*$",  # "warszawa też?"
        ]

        for pattern in reference_patterns:
            match = re.match(pattern, message_lower)
            if match:
                referenced_item = match.group(1).strip()
                return self._expand_reference(
                    referenced_item, context_memory, message_history, session_id
                )

        # No reference found, return original
        return current_message

    def _expand_reference(
        self,
        referenced_item: str,
        context_memory: Dict,
        message_history: List[Dict],
        session_id: str,
    ) -> str:
        """Expand reference to full question"""

        # Get last bot response to understand context
        last_bot_msg = self._get_last_bot_message(message_history)

        # Check what was being discussed
        if self._is_discussing_packages(last_bot_msg):
            return f"Jaki jest koszt pakietu {referenced_item}?"

        if self._is_discussing_cities(last_bot_msg):
            return f"Czy działacie w {referenced_item}?"

        if self._is_discussing_prices(last_bot_msg):
            return f"Ile kosztuje {referenced_item}?"

        if self._is_discussing_timeline(last_bot_msg):
            return f"Jak długo trwa {referenced_item}?"

        # Generic expansion based on keywords
        if any(
            word in referenced_item
            for word in ["pakiet", "srebrny", "złoty", "platynowy", "silver", "gold", "platinum"]
        ):
            return f"Jaki jest koszt pakietu {referenced_item}?"

        if any(
            word in referenced_item
            for word in ["warszawa", "kraków", "wrocław", "poznań", "gdańsk"]
        ):
            return f"Czy działacie w {referenced_item}?"

        # Fallback - assume same type of question as before
        if last_bot_msg:
            if "koszt" in last_bot_msg or "cena" in last_bot_msg or "zł" in last_bot_msg:
                return f"Ile kosztuje {referenced_item}?"
            if "czas" in last_bot_msg or "długo" in last_bot_msg or "termin" in last_bot_msg:
                return f"Jak długo trwa {referenced_item}?"

        return f"Opowiedz mi o {referenced_item}"

    def _get_last_bot_message(self, message_history: List[Dict]) -> Optional[str]:
        """Get last bot message from history"""
        for msg in reversed(message_history):
            if msg.get("sender") == "bot":
                return msg.get("message", "").lower()
        return None

    def _is_discussing_packages(self, text: str) -> bool:
        """Check if discussing packages"""
        if not text:
            return False
        keywords = ["pakiet", "srebrny", "złoty", "platynowy", "wykończenie", "package"]
        return any(keyword in text for keyword in keywords)

    def _is_discussing_cities(self, text: str) -> bool:
        """Check if discussing cities/locations"""
        if not text:
            return False
        keywords = ["miasto", "region", "działamy", "obsługujemy", "gdzie", "city", "location"]
        return any(keyword in text for keyword in keywords)

    def _is_discussing_prices(self, text: str) -> bool:
        """Check if discussing prices"""
        if not text:
            return False
        keywords = ["koszt", "cena", "ile", "zł", "price", "cost"]
        return any(keyword in text for keyword in keywords)

    def _is_discussing_timeline(self, text: str) -> bool:
        """Check if discussing timeline"""
        if not text:
            return False
        keywords = ["czas", "długo", "termin", "kiedy", "duration", "time"]
        return any(keyword in text for keyword in keywords)

    def track_topic(self, session_id: str, topic: str, details: str):
        """Track current topic for future reference"""
        if session_id not in self.session_context:
            self.session_context[session_id] = []

        self.session_context[session_id].append({"topic": topic, "details": details})

        # Keep only last 5 topics
        if len(self.session_context[session_id]) > 5:
            self.session_context[session_id].pop(0)


# Global instance
multi_turn_dialog = MultiTurnDialogService()
