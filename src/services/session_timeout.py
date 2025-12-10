"""
Session Timeout & Reengagement Service
Gentle nudges when user goes inactive during conversation

Uses Redis TTL for production (scalable across instances).
Falls back to in-memory dict for development.
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
        # Fallback for dev (replaced by Redis in production)
        self._fallback_sessions = {}
        self._fallback_nudges = {}

        # Lazy-load Redis cache
        self._cache = None

    @property
    def cache(self):
        """Lazy-load Redis cache to avoid import deadlock"""
        if self._cache is None:
            from src.services.redis_service import get_redis_cache

            self._cache = get_redis_cache()
        return self._cache

    # Backward-compatible properties for tests
    @property
    def active_sessions(self):
        """Backward compatibility: expose fallback sessions"""
        return self._fallback_sessions

    @property
    def nudge_sent(self):
        """Backward compatibility: expose fallback nudges"""
        return self._fallback_nudges

    def update_activity(self, session_id: str):
        """
        Update last activity timestamp for session

        Uses Redis with TTL = SESSION_TIMEOUT_MINUTES for automatic cleanup.
        Stores ISO timestamp string for easy deserialization.
        Also updates fallback for backward compatibility with tests.
        """
        now_dt = datetime.now(timezone.utc)
        now = now_dt.isoformat()
        key = f"session:activity:{session_id}"
        ttl_seconds = self.SESSION_TIMEOUT_MINUTES * 60

        # Always update fallback for backward compatibility
        self._fallback_sessions[session_id] = now_dt

        # Try Redis (will use internal fallback if Redis unavailable)
        try:
            self.cache.set(key, now, ttl=ttl_seconds)
        except Exception as e:
            logger.warning(f"Redis update failed: {e}")

    def check_inactivity(self, session_id: str) -> Optional[Dict]:
        """
        Check if session is inactive and needs nudge

        Returns:
            dict with nudge message or None
        """
        key = f"session:activity:{session_id}"

        try:
            last_activity_str = self.cache.get(key)
            if not last_activity_str:
                # Try fallback
                if session_id not in self._fallback_sessions:
                    return None
                last_activity = self._fallback_sessions[session_id]
            else:
                last_activity = datetime.fromisoformat(last_activity_str)
        except Exception as e:
            logger.warning(f"Redis get failed, using fallback: {e}")
            if session_id not in self._fallback_sessions:
                return None
            last_activity = self._fallback_sessions[session_id]

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
        """
        Check if nudge was already sent for this inactivity period

        Uses Redis with 5-minute TTL to prevent duplicate nudges.
        Also syncs with _fallback_nudges for backward compatibility.
        """
        key = f"session:nudge:{session_id}"
        now_dt = datetime.now(timezone.utc)

        try:
            existing_nudge = self.cache.get(key)
            if not existing_nudge:
                # No nudge sent recently - mark as sent with 5 min TTL
                self.cache.set(key, now_dt.isoformat(), ttl=300)
                # Also update fallback for consistency
                self._fallback_nudges[session_id] = now_dt
                return False

            # Nudge was sent recently
            return True
        except Exception as e:
            logger.warning(f"Redis nudge check failed, using fallback: {e}")

            # Fallback logic
            if session_id not in self._fallback_nudges:
                self._fallback_nudges[session_id] = now_dt
                return False

            time_since_nudge = (now_dt - self._fallback_nudges[session_id]).total_seconds() / 60
            if time_since_nudge < 5:
                return True

            self._fallback_nudges[session_id] = now_dt
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
        """
        Check if session is still considered active

        Leverages Redis TTL: if key exists, session is active.
        """
        key = f"session:activity:{session_id}"

        try:
            last_activity_str = self.cache.get(key)
            if not last_activity_str:
                # Try fallback
                if session_id not in self._fallback_sessions:
                    return False
                last_activity = self._fallback_sessions[session_id]
            else:
                # If Redis has key, session is active (TTL not expired)
                return True
        except Exception as e:
            logger.warning(f"Redis check failed, using fallback: {e}")
            if session_id not in self._fallback_sessions:
                return False
            last_activity = self._fallback_sessions[session_id]

        # Fallback calculation
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
        """
        Remove sessions older than timeout

        Redis: Auto-cleanup via TTL (no manual cleanup needed).
        Fallback: Manual cleanup for in-memory dict.
        """
        # Redis handles TTL automatically - only clean fallback
        if not self._fallback_sessions:
            return

        now = datetime.now(timezone.utc)
        timeout = timedelta(minutes=self.SESSION_TIMEOUT_MINUTES)

        to_remove = [
            sid
            for sid, last_activity in self._fallback_sessions.items()
            if now - last_activity > timeout
        ]

        for sid in to_remove:
            del self._fallback_sessions[sid]
            if sid in self._fallback_nudges:
                del self._fallback_nudges[sid]

        if to_remove:
            logger.info(f"Cleaned up {len(to_remove)} inactive sessions from fallback storage")


# Global instance
session_timeout_service = SessionTimeoutService()
