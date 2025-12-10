"""
Follow-up Automation Service
Handles abandoned conversations and automated re-engagement
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from src.models.chatbot import ChatConversation, ChatMessage, db

logger = logging.getLogger(__name__)


class FollowUpAutomationService:
    """Automated follow-ups for abandoned conversations"""

    # Timing rules
    FIRST_FOLLOWUP_HOURS = 24  # After 24 hours
    SECOND_FOLLOWUP_HOURS = 72  # After 3 days
    FINAL_FOLLOWUP_HOURS = 168  # After 7 days

    def get_conversations_needing_followup(self) -> List[Dict]:
        """
        Find conversations that need follow-up

        RODO Compliance: Only includes conversations with explicit marketing consent.
        Users must have either:
        - rodo_consent = True (explicit RODO agreement)
        - marketing_consent = True (marketing follow-ups allowed)

        Returns:
            List of conversations with suggested follow-up messages
        """
        now = datetime.now(timezone.utc)

        # Get conversations from last 7 days that haven't ended
        cutoff_date = now - timedelta(days=7)

        conversations = ChatConversation.query.filter(
            ChatConversation.started_at >= cutoff_date,
            ChatConversation.ended_at.is_(None),  # Not ended
            ChatConversation.context_data.isnot(None),  # Has some context
            # RODO: Require explicit consent for automated marketing messages
            ChatConversation.rodo_consent == True,  # noqa: E712
        ).all()

        followups = []

        for conv in conversations:
            # Get last message timestamp
            last_msg = (
                ChatMessage.query.filter_by(conversation_id=conv.id)
                .order_by(ChatMessage.timestamp.desc())
                .first()
            )

            if not last_msg:
                continue

            hours_since = (now - last_msg.timestamp).total_seconds() / 3600

            # Check if already sent follow-ups
            sent_followups = conv.followup_count or 0

            # Determine if follow-up needed
            followup_data = self._check_followup_timing(hours_since, sent_followups, conv)

            if followup_data:
                followups.append(followup_data)

        return followups

    def _check_followup_timing(
        self, hours_since: float, sent_followups: int, conversation: ChatConversation
    ) -> Optional[Dict]:
        """Check if follow-up is needed based on timing"""

        import json

        context = json.loads(conversation.context_data or "{}")

        # First follow-up
        if sent_followups == 0 and hours_since >= self.FIRST_FOLLOWUP_HOURS:
            message = self._generate_first_followup(context, conversation)
            return {
                "conversation_id": conversation.id,
                "session_id": conversation.session_id,
                "followup_number": 1,
                "message": message,
                "context": context,
            }

        # Second follow-up
        if sent_followups == 1 and hours_since >= self.SECOND_FOLLOWUP_HOURS:
            message = self._generate_second_followup(context, conversation)
            return {
                "conversation_id": conversation.id,
                "session_id": conversation.session_id,
                "followup_number": 2,
                "message": message,
                "context": context,
            }

        # Final follow-up
        if sent_followups == 2 and hours_since >= self.FINAL_FOLLOWUP_HOURS:
            message = self._generate_final_followup(context, conversation)
            return {
                "conversation_id": conversation.id,
                "session_id": conversation.session_id,
                "followup_number": 3,
                "message": message,
                "context": context,
            }

        return None

    def _generate_first_followup(self, context: Dict, conversation: ChatConversation) -> str:
        """Generate first follow-up message (24h)"""
        name = context.get("name", "tam")

        # Personalized based on what was discussed
        if context.get("package"):
            package = context["package"]
            sqm = context.get("square_meters", "Twojego mieszkania")
            return f"Cześć{' ' + name if name != 'tam' else ''}! 👋\n\nWidzę że interesował Cię pakiet {package}{f' dla {sqm}m²' if sqm != 'Twojego mieszkania' else ''}. Chętnie przygotuję szczegółową wycenę - czy mogę wysłać ją na email?"

        if context.get("city"):
            city = context["city"]
            return f"Cześć{' ' + name if name != 'tam' else ''}! 👋\n\nPytałeś o wykończenie w {city}. Mamy tam kilka aktywnych projektów - chcesz zobaczyć nasze realizacje w Twojej okolicy?"

        # Generic
        return f"Cześć{' ' + name if name != 'tam' else ''}! 👋\n\nWracam do naszej rozmowy o wykończeniu. Mogę pomóc w przygotowaniu wyceny lub odpowiedzieć na pytania. Daj znać!"

    def _generate_second_followup(self, context: Dict, conversation: ChatConversation) -> str:
        """Generate second follow-up message (3 days)"""
        name = context.get("name", "")

        # More direct - offer meeting
        if context.get("square_meters") and context.get("package"):
            sqm = context["square_meters"]
            package = context["package"]
            return f"Cześć{' ' + name if name else ''}! 😊\n\nWciąż aktualna jest oferta {package} dla {sqm}m²? Mogę umówić Cię na bezpłatną konsultację z naszym doradcą - najbliższe terminy to jutro lub pojutrze. Interesuje Cię?"

        # Offer portfolio/references
        return f"Cześć{' ' + name if name else ''}! 😊\n\nMamy właśnie ukończone nowe projekty - mogę pokazać zdjęcia i opinie klientów. Zainteresowany?"

    def _generate_final_followup(self, context: Dict, conversation: ChatConversation) -> str:
        """Generate final follow-up message (7 days)"""
        name = context.get("name", "")

        # Last chance - special offer or urgency
        return f"Cześć{' ' + name if name else ''}! 🎁\n\nTo moja ostatnia wiadomość - nie chcę być natrętny 😊\n\nJeśli wciąż myślisz o wykończeniu, mamy specjalną promocję w tym miesiącu. Daj znać jeśli chcesz poznać szczegóły!\n\nPozdrawiam,\nZespół NovaHouse"

    def mark_followup_sent(self, conversation_id: int):
        """Mark that follow-up was sent"""
        conversation = ChatConversation.query.get(conversation_id)
        if conversation:
            if not hasattr(conversation, "followup_count") or conversation.followup_count is None:
                conversation.followup_count = 0
            conversation.followup_count += 1
            conversation.last_followup_at = datetime.now(timezone.utc)
            db.session.commit()

    def send_followup(self, followup_data: Dict) -> bool:
        """
        Send follow-up message to user (IDEMPOTENT)

        RODO Compliance: Validates consent before sending automated messages.
        Will NOT send if user hasn't explicitly consented to marketing communication.

        IDEMPOTENCY: Uses FollowupEvent table to prevent duplicate sends.
        - Atomic check-insert pattern: INSERT followup_event FIRST
        - If IntegrityError (duplicate): Skip (already sent)
        - If success: Send message + commit

        Args:
            followup_data: Dict with conversation_id, session_id, message, followup_number

        Returns:
            True if sent successfully, False if consent missing, already sent, or error
        """
        from sqlalchemy.exc import IntegrityError

        from src.models.followup_event import FollowupEvent

        try:
            conversation_id = followup_data["conversation_id"]
            message = followup_data["message"]
            followup_number = followup_data.get("followup_number", 1)

            # RODO: Double-check consent before sending
            conversation = ChatConversation.query.get(conversation_id)
            if not conversation or not conversation.rodo_consent:
                logger.warning(
                    f"RODO: Skipping follow-up for conversation {conversation_id} - "
                    f"no marketing consent (rodo_consent={getattr(conversation, 'rodo_consent', None)})"
                )
                return False

            # IDEMPOTENCY: Check if already sent (atomic INSERT with UNIQUE constraint)
            try:
                followup_event = FollowupEvent(
                    conversation_id=conversation_id,
                    followup_number=followup_number,
                    sent_at=datetime.now(timezone.utc),
                    status="sent",
                )
                db.session.add(followup_event)
                db.session.flush()  # Force UNIQUE check before sending
            except IntegrityError:
                db.session.rollback()
                logger.info(
                    f"⏩ Skipping follow-up #{followup_number} for conversation {conversation_id} - already sent"
                )
                return False

            # Save follow-up message (only if event INSERT succeeded)
            followup_msg = ChatMessage(
                conversation_id=conversation_id,
                message=message,
                sender="bot",
                timestamp=datetime.now(timezone.utc),
                is_followup=True,  # Mark as automated follow-up
            )
            db.session.add(followup_msg)

            # Mark as sent
            self.mark_followup_sent(conversation_id)

            db.session.commit()

            logger.info(f"✅ Sent follow-up #{followup_number} to {followup_data['session_id']}")
            return True

        except Exception as e:
            logger.error(f"Error sending follow-up: {e}", exc_info=True)
            db.session.rollback()
            return False

    def get_high_value_abandoned(self) -> List[Dict]:
        """
        Get high-value abandoned conversations (had package/sqm but no email)

        Returns:
            List of high-priority follow-ups
        """
        import json

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=48)

        conversations = ChatConversation.query.filter(
            ChatConversation.started_at >= cutoff, ChatConversation.ended_at.is_(None)
        ).all()

        high_value = []

        for conv in conversations:
            context = json.loads(conv.context_data or "{}")

            # Has package and sqm but no email = high value
            if context.get("package") and context.get("square_meters") and not context.get("email"):
                last_msg = (
                    ChatMessage.query.filter_by(conversation_id=conv.id)
                    .order_by(ChatMessage.timestamp.desc())
                    .first()
                )

                if last_msg:
                    hours_since = (now - last_msg.timestamp).total_seconds() / 3600

                    high_value.append(
                        {
                            "conversation_id": conv.id,
                            "session_id": conv.session_id,
                            "context": context,
                            "hours_since": hours_since,
                            "estimated_value": self._estimate_value(context),
                        }
                    )

        # Sort by value
        high_value.sort(key=lambda x: x["estimated_value"], reverse=True)

        return high_value

    def _estimate_value(self, context: Dict) -> float:
        """Estimate conversation value for prioritization"""
        value = 0

        if context.get("package"):
            package = context["package"].lower()
            if "platynowy" in package or "platinum" in package:
                value += 5000
            elif "złoty" in package or "gold" in package:
                value += 3500
            else:
                value += 2000

        if context.get("square_meters"):
            value *= context["square_meters"]

        return value


# Global instance
followup_automation = FollowUpAutomationService()
