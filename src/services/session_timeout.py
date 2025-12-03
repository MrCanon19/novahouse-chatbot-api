"""
Session Timeout & Reengagement Service
Gentle nudges when user goes inactive during conversation
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class SessionTimeoutService:
    """Handle session timeouts and reengagement"""

    # Timeout thresholds
    GENTLE_NUDGE_MINUTES = 3  # After 3 minutes of silence
    SESSION_TIMEOUT_MINUTES = 30  # After 30 minutes, consider session ended

    def __init__(self):
        self.active_sessions = {}  # Track last activity per session
        self.nudge_sent = {}  # Track sent nudges per session

    def update_activity(self, session_id: str):
        """Update last activity timestamp for session"""
        self.active_sessions[session_id] = datetime.now(timezone.utc)

    def check_inactivity(self, session_id: str) -> Optional[Dict]:
        """
        Check if session is inactive and needs nudge

        Returns:
            dict with nudge message or None
        """
        if session_id not in self.active_sessions:
            return None

        last_activity = self.active_sessions[session_id]
        now = datetime.now(timezone.utc)
        minutes_inactive = (now - last_activity).total_seconds() / 60

        # Gentle nudge after 3 minutes
        if self.GENTLE_NUDGE_MINUTES <= minutes_inactive < self.SESSION_TIMEOUT_MINUTES:
            # Check if nudge already sent
            if not self._nudge_already_sent(session_id):
                return {
                    "type": "gentle_nudge",
                    "message": self._get_nudge_message(session_id),
                    "minutes_inactive": minutes_inactive,
                }

        # Session timeout
        if minutes_inactive >= self.SESSION_TIMEOUT_MINUTES:
            return {
                "type": "session_timeout",
                "message": self._get_timeout_message(session_id),
                "minutes_inactive": minutes_inactive,
            }

        return None

    def _nudge_already_sent(self, session_id: str) -> bool:
        """Check if nudge was already sent for this inactivity period"""
        if session_id not in self.nudge_sent:
            self.nudge_sent[session_id] = datetime.now(timezone.utc)
            return False

        # Check if nudge was sent recently (within last 5 minutes)
        time_since_nudge = (
            datetime.now(timezone.utc) - self.nudge_sent[session_id]
        ).total_seconds() / 60
        if time_since_nudge < 5:
            return True

        # Update timestamp and allow new nudge
        self.nudge_sent[session_id] = datetime.now(timezone.utc)
        return False

    def _get_nudge_message(self, session_id: str) -> str:
        """Get gentle reengagement message"""
        messages = [
            "Jesteś jeszcze tam? 😊",
            "Mogę coś jeszcze wyjaśnić?",
            "Masz jakieś pytania? Chętnie pomogę! 💬",
            "Czy wszystko jasne? Daj znać jeśli potrzebujesz pomocy!",
            "Wciąż tu jestem jeśli chcesz porozmawiać 👋",
        ]

        # Simple rotation based on session
        index = hash(session_id) % len(messages)
        return messages[index]

    def _get_timeout_message(self, session_id: str) -> str:
        """Get session timeout message"""
        return (
            "Rozumiem że potrzebujesz czasu na przemyślenie 😊\n\n"
            "Gdy będziesz gotowy do rozmowy, napisz - chętnie pomogę!\n\n"
            "Możesz też od razu umówić się na konsultację: NovaHouse.pl/kontakt"
        )

    def is_session_active(self, session_id: str) -> bool:
        """Check if session is still considered active"""
        if session_id not in self.active_sessions:
            return False

        last_activity = self.active_sessions[session_id]
        now = datetime.now(timezone.utc)
        minutes_inactive = (now - last_activity).total_seconds() / 60

        return minutes_inactive < self.SESSION_TIMEOUT_MINUTES

    def get_reengagement_suggestion(self, context_memory: Dict) -> Optional[str]:
        """
        Get smart reengagement suggestion based on conversation state

        Returns:
            Contextual nudge message
        """
        # If had package interest
        if context_memory.get("package"):
            package = context_memory["package"]
            return f"💎 Widzę że interesuje Cię pakiet {package}. Mogę wysłać szczegółową wycenę na email?"

        # If had sqm but no package
        if context_memory.get("square_meters") and not context_memory.get("package"):
            sqm = context_memory["square_meters"]
            return f"📐 Dla {sqm}m² mogę polecić kilka pakietów. Chcesz poznać opcje?"

        # If had city but nothing else
        if context_memory.get("city") and not context_memory.get("square_meters"):
            city = context_memory["city"]
            return f"📍 Świetnie że jesteś z {city}! Jaki metraż ma Twoje mieszkanie?"

        # Generic
        return "🏠 Mogę pomóc w wyborze pakietu wykończenia. Co Cię najbardziej interesuje?"

    def cleanup_old_sessions(self):
        """Remove sessions older than timeout"""
        now = datetime.now(timezone.utc)
        timeout = timedelta(minutes=self.SESSION_TIMEOUT_MINUTES)

        to_remove = [
            sid
            for sid, last_activity in self.active_sessions.items()
            if now - last_activity > timeout
        ]

        for sid in to_remove:
            del self.active_sessions[sid]

        if to_remove:
            logger.info(f"Cleaned up {len(to_remove)} inactive sessions")


# Global instance
session_timeout_service = SessionTimeoutService()
