"""
Session Timeout Service
Handles session inactivity, nudges, and cleanup.
Redis is used as cache, but DB is the source of truth.
"""
import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict

import json
from src.models.chatbot import ChatConversation, ChatMessage, db

logger = logging.getLogger(__name__)

# Configuration from environment
INACTIVITY_MINUTES_BEFORE_NUDGE = int(os.getenv("INACTIVITY_MINUTES_BEFORE_NUDGE", "15"))  # 15 min
INACTIVITY_MINUTES_BEFORE_TIMEOUT = int(os.getenv("INACTIVITY_MINUTES_BEFORE_TIMEOUT", "30"))  # 30 min


class SessionTimeoutService:
    """
    Service for managing session timeouts, nudges, and cleanup.
    Uses DB as source of truth, Redis only as cache.
    """
    
    # Configuration
    INACTIVITY_MINUTES_BEFORE_NUDGE = INACTIVITY_MINUTES_BEFORE_NUDGE
    INACTIVITY_MINUTES_BEFORE_TIMEOUT = INACTIVITY_MINUTES_BEFORE_TIMEOUT
    
    def __init__(self):
        self.redis_client = None
        self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis client (optional, for caching)"""
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            try:
                import redis
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                )
                self.redis_client.ping()
                logger.info("✅ SessionTimeoutService using Redis cache")
            except Exception as e:
                logger.warning(f"⚠️  Redis unavailable for session timeout, using DB only: {e}")
                self.redis_client = None
        else:
            logger.info("ℹ️  Redis not configured, using DB only")
    
    def get_last_activity(self, session_id: str) -> Optional[datetime]:
        """
        Get last activity timestamp for session.
        Checks Redis cache first, then DB.
        """
        # Try Redis cache
        if self.redis_client:
            try:
                cached = self.redis_client.get(f"session:last_activity:{session_id}")
                if cached:
                    return datetime.fromisoformat(cached)
            except Exception as e:
                logger.warning(f"Redis cache read failed: {e}")
        
        # Fallback to DB
        try:
            last_message = (
                db.session.query(ChatMessage)
                .join(ChatConversation)
                .filter(ChatConversation.session_id == session_id)
                .order_by(ChatMessage.timestamp.desc())
                .first()
            )
            
            if last_message:
                last_activity = last_message.timestamp
                # Cache in Redis
                if self.redis_client:
                    try:
                        self.redis_client.setex(
                            f"session:last_activity:{session_id}",
                            3600,  # 1 hour cache
                            last_activity.isoformat()
                        )
                    except Exception:
                        pass
                return last_activity
            
            # Check conversation start time
            conversation = ChatConversation.query.filter_by(session_id=session_id).first()
            if conversation:
                return conversation.started_at
            
            return None
        except Exception as e:
            logger.error(f"Error getting last activity for session {session_id}: {e}")
            return None
    
    def update_activity(self, session_id: str):
        """Update last activity timestamp (called on each message)"""
        now = datetime.now(timezone.utc)
        
        # Update Redis cache
        if self.redis_client:
            try:
                self.redis_client.setex(
                    f"session:last_activity:{session_id}",
                    3600,
                    now.isoformat()
                )
            except Exception as e:
                logger.warning(f"Redis cache update failed: {e}")
        
        # DB is updated automatically when message is saved
        # This is just for cache invalidation
    
    def should_send_nudge(self, session_id: str) -> bool:
        """
        Check if nudge should be sent (inactive for X minutes, not yet nudged).
        Returns True if session is inactive and hasn't been nudged yet.
        """
        last_activity = self.get_last_activity(session_id)
        if not last_activity:
            return False
        
        inactive_minutes = (datetime.now(timezone.utc) - last_activity).total_seconds() / 60
        
        if inactive_minutes < INACTIVITY_MINUTES_BEFORE_NUDGE:
            return False
        
        # Check if already nudged (check in context_data or last bot message)
        conversation = ChatConversation.query.filter_by(session_id=session_id).first()
        if conversation:
            context_data = json.loads(conversation.context_data or "{}")
            if context_data.get("nudge_sent"):
                return False
            
            # Also check if last bot message was a nudge
            last_bot_message = (
                db.session.query(ChatMessage)
                .filter_by(conversation_id=conversation.id, sender="bot")
                .order_by(ChatMessage.timestamp.desc())
                .first()
            )
            if last_bot_message and "przerwałeś rozmowę" in last_bot_message.message.lower():
                return False
        
        return True
    
    def send_nudge(self, session_id: str) -> bool:
        """
        Send nudge message to inactive session.
        Returns True if nudge was sent successfully.
        """
        try:
            conversation = ChatConversation.query.filter_by(session_id=session_id).first()
            if not conversation:
                return False
            
            # Mark as nudged in context_data
            context_data = json.loads(conversation.context_data or "{}")
            context_data["nudge_sent"] = True
            context_data["nudge_sent_at"] = datetime.now(timezone.utc).isoformat()
            conversation.context_data = json.dumps(context_data)
            
            # Create nudge message
            nudge_message = ChatMessage(
                conversation_id=conversation.id,
                message="Cześć! Widzę, że przerwałeś rozmowę. Czy mogę jeszcze w czymś pomóc? 😊",
                sender="bot",
                timestamp=datetime.now(timezone.utc),
            )
            
            db.session.add(nudge_message)
            db.session.commit()
            
            logger.info(f"✅ Nudge sent to session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending nudge to session {session_id}: {e}")
            db.session.rollback()
            return False
    
    def is_timed_out(self, session_id: str) -> bool:
        """Check if session has timed out (inactive for X minutes)"""
        last_activity = self.get_last_activity(session_id)
        if not last_activity:
            return False
        
        inactive_minutes = (datetime.now(timezone.utc) - last_activity).total_seconds() / 60
        return inactive_minutes >= INACTIVITY_MINUTES_BEFORE_TIMEOUT
    
    def cleanup_old_sessions(self, older_than_hours: int = 24) -> Dict:
        """
        Clean up old inactive sessions from DB.
        Marks them as ended for analytics.
        
        Args:
            older_than_hours: Clean up sessions inactive for more than X hours
            
        Returns:
            Dict with cleanup stats
        """
        try:
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=older_than_hours)
            
            # Find inactive sessions
            inactive_sessions = (
                db.session.query(ChatConversation)
                .filter(
                    ChatConversation.ended_at.is_(None),
                    ChatConversation.started_at < cutoff_time
                )
                .all()
            )
            
            cleaned_count = 0
            for session in inactive_sessions:
                # Check if really inactive (no recent messages)
                last_message = (
                    db.session.query(ChatMessage)
                    .filter_by(conversation_id=session.id)
                    .order_by(ChatMessage.timestamp.desc())
                    .first()
                )
                
                if last_message and last_message.timestamp < cutoff_time:
                    session.ended_at = datetime.now(timezone.utc)
                    # Update context_data with status
                    context_data = json.loads(session.context_data or "{}")
                    context_data["status"] = "timeout"
                    session.context_data = json.dumps(context_data)
                    cleaned_count += 1
                    
                    # Clear Redis cache
                    if self.redis_client:
                        try:
                            self.redis_client.delete(f"session:last_activity:{session.session_id}")
                        except Exception:
                            pass
            
            db.session.commit()
            
            logger.info(f"✅ Cleaned up {cleaned_count} old sessions")
            
            return {
                "cleaned_count": cleaned_count,
                "cutoff_time": cutoff_time.isoformat(),
                "older_than_hours": older_than_hours,
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")
            db.session.rollback()
            return {
                "cleaned_count": 0,
                "error": str(e),
            }
    
    def get_inactive_sessions_needing_nudge(self) -> List[Dict]:
        """Get list of sessions that need nudge"""
        try:
            # Get all active sessions
            active_sessions = (
                db.session.query(ChatConversation)
                .filter(ChatConversation.ended_at.is_(None))
                .all()
            )
            
            sessions_needing_nudge = []
            for session in active_sessions:
                if self.should_send_nudge(session.session_id):
                    last_activity = self.get_last_activity(session.session_id)
                    sessions_needing_nudge.append({
                        "session_id": session.session_id,
                        "last_activity": last_activity.isoformat() if last_activity else None,
                        "inactive_minutes": (
                            (datetime.now(timezone.utc) - last_activity).total_seconds() / 60
                            if last_activity else 0
                        ),
                    })
            
            return sessions_needing_nudge
            
        except Exception as e:
            logger.error(f"Error getting sessions needing nudge: {e}")
            return []


# Global instance
session_timeout_service = SessionTimeoutService()

