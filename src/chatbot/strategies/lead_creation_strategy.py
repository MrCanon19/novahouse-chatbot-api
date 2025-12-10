from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from src.integrations.monday_client import MondayClient
from src.models.chatbot import ChatConversation, ChatMessage, CompetitiveIntel, Lead
from src.services.email_service import EmailService

from .base import ChatStrategy


# Placeholder for functions that need to be moved from chatbot.py
def calculate_lead_score(context_memory: Dict[str, Any], message_count: int) -> int:
    """
    (PLACEHOLDER - TO BE MOVED TO DEDICATED LEAD SCORING SERVICE)
    Calculates a lead score based on extracted context and conversation length.
    """
    base_score = 0
    if context_memory.get("name"):
        base_score += 10
    if context_memory.get("email"):
        base_score += 10
    if context_memory.get("phone"):
        base_score += 10
    if context_memory.get("city"):
        base_score += 10
    if context_memory.get("square_meters"):
        base_score += 10
    if context_memory.get("package"):
        base_score += 15

    score = base_score
    if base_score > 0:
        score += min(message_count * 2, 10)

    return min(score, 100)


def generate_conversation_summary(
    messages: List[ChatMessage], context_memory: Dict[str, Any]
) -> str:
    """
    (PLACEHOLDER - TO BE MOVED TO DEDICATED SUMMARY SERVICE)
    Generates a summary of the conversation.
    """
    summary = "Konwersacja z chatbotem:\n"
    for msg in messages:
        text = getattr(msg, "message", getattr(msg, "text", ""))
        sender = getattr(msg, "sender", "user") or "user"
        summary += f"{sender.capitalize()}: {text}\n"
    summary += "\nZebrane dane:\n"
    for key, value in context_memory.items():
        summary += f"- {key}: {value}\n"
    return summary


def suggest_next_best_action(context_memory: Dict[str, Any], lead_score: int) -> str:
    """
    (PLACEHOLDER - TO BE MOVED TO DEDICATED LEAD SERVICE)
    Suggests the next best action for a lead based on score and context.
    """
    if lead_score >= 70 and (context_memory.get("email") or context_memory.get("phone")):
        return "HIGH PRIORITY: Call within 1 hour and send tailored offer via email."
    if lead_score >= 50:
        return "Follow-up via email within 24h with a tailored proposal."
    return "Nurture via newsletter and light touch follow-ups."


class LeadCreationStrategy(ChatStrategy):
    """
    A strategy to check if enough information has been collected to create a lead,
    handle user confirmation, and then create the lead in the database and Monday.com.
    """

    def __init__(
        self,
        db_session: Session,
        monday_client: MondayClient,
        email_service: EmailService,
        admin_email: str,
    ):
        self.db_session = db_session
        self.monday_client = monday_client
        self.email_service = email_service
        self.admin_email = admin_email

    def _check_data_confirmation_intent(self, user_message: str) -> Optional[str]:
        """
        (PLACEHOLDER - TO BE MOVED TO DEDICATED INTENT SERVICE)
        Detects if the user wants to confirm or edit the collected data.
        """
        message_lower = user_message.lower()
        if (
            "tak" in message_lower
            or "potwierdzam" in message_lower
            or "zgadza się" in message_lower
        ):
            return "confirm"
        if "nie" in message_lower or "popraw" in message_lower or "zmień" in message_lower:
            return "edit"
        return None

    def _format_data_confirmation_message(self, context_memory: Dict[str, Any]) -> str:
        """
        (PLACEHOLDER - TO BE MOVED TO DEDICATED FORMATTING SERVICE)
        Formats a message asking the user to confirm collected data.
        """
        message = "Czy te dane są poprawne? Proszę potwierdź lub wskaż co poprawić:\n"
        if context_memory.get("name"):
            message += f"- Imię: {context_memory['name']}\n"
        if context_memory.get("email"):
            message += f"- E-mail: {context_memory['email']}\n"
        if context_memory.get("phone"):
            message += f"- Telefon: {context_memory['phone']}\n"
        if context_memory.get("city"):
            message += f"- Miasto: {context_memory['city']}\n"
        if context_memory.get("square_meters"):
            message += f"- Metraż: {context_memory['square_meters']}m²\n"
        if context_memory.get("package"):
            message += f"- Interesujący pakiet: {context_memory['package']}\n"
        message += "\n(Potwierdź wpisując 'tak' lub 'popraw' jeśli chcesz zmienić dane.)"
        return message

    def _should_ask_for_confirmation(
        self, context_memory: Dict[str, Any], conversation: ChatConversation
    ) -> bool:
        """
        (PLACEHOLDER - TO BE MOVED TO DEDICATED LEAD SERVICE)
        Determines if the bot should ask the user to confirm collected data.
        """
        has_contact_data = context_memory.get("name") and (
            context_memory.get("email") or context_memory.get("phone")
        )
        return has_contact_data and not conversation.awaiting_confirmation

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes lead creation logic based on collected context and user intent.

        Args:
            context: The current chat context, containing 'user_message',
                     'session_id', 'conversation', and 'context_memory'.

        Returns:
            The updated context, potentially with 'bot_response' and
            updated 'conversation' object (e.g., awaiting_confirmation flag).
        """
        user_message = context.get("user_message")
        session_id = context.get("session_id")
        conversation: ChatConversation = context.get("conversation")
        context_memory = context.get("context_memory", {})
        bot_response = context.get("bot_response")  # Response from previous strategies

        # --- Lead Confirmation / Creation Logic ---
        confirmation_intent = self._check_data_confirmation_intent(user_message)
        existing_lead = self.db_session.query(Lead).filter_by(session_id=session_id).first()
        has_enough_data_for_lead = context_memory.get("name") and (
            context_memory.get("email") or context_memory.get("phone")
        )

        if confirmation_intent == "confirm" and has_enough_data_for_lead and not existing_lead:
            # User confirmed - create lead now
            try:
                # Get message count for lead scoring
                message_count = (
                    self.db_session.query(ChatMessage)
                    .filter_by(conversation_id=conversation.id)
                    .count()
                )
                lead_score = calculate_lead_score(context_memory, message_count)

                # Generate conversation summary
                all_messages = (
                    self.db_session.query(ChatMessage)
                    .filter_by(conversation_id=conversation.id)
                    .order_by(ChatMessage.timestamp.asc())
                    .all()
                )
                conv_summary = generate_conversation_summary(all_messages, context_memory)

                # Create lead
                lead = Lead(
                    session_id=session_id,
                    name=context_memory.get("name", "Unknown"),
                    email=context_memory.get("email"),
                    phone=context_memory.get("phone"),
                    location=context_memory.get("city"),
                    property_size=context_memory.get("square_meters"),
                    interested_package=context_memory.get("package"),
                    source="chatbot",
                    status="qualified",  # User confirmed data
                    lead_score=lead_score,
                    conversation_summary=conv_summary,
                    data_confirmed=True,
                    last_interaction=datetime.now(timezone.utc),
                )

                self.db_session.add(lead)
                self.db_session.flush()  # Flush to get lead.id before Monday call

                # Generate next action recommendation
                next_action = suggest_next_best_action(context_memory, lead_score)
                lead.notes = f"Next Action: {next_action}"

                # Check for competitive mentions
                competitor_intel = (
                    self.db_session.query(CompetitiveIntel)
                    .filter_by(session_id=session_id)
                    .order_by(CompetitiveIntel.created_at.desc())
                    .first()
                )
                competitor_name = competitor_intel.competitor_name if competitor_intel else None

                # Sync with Monday.com
                monday_item_id = self.monday_client.create_lead_item(
                    {
                        "name": lead.name,
                        "email": lead.email,
                        "phone": lead.phone,
                        "message": f"Lead Score: {lead_score}/100 | {conv_summary} | Action: {next_action}",
                        "property_type": "Mieszkanie",  # Defaulting, can be dynamic
                        "budget": context_memory.get("square_meters", ""),
                        "lead_score": lead_score,
                        "competitor_mentioned": competitor_name,
                        "next_action": next_action,
                    }
                )

                if monday_item_id:
                    lead.monday_item_id = monday_item_id
                    print(
                        f"[Monday] Confirmed lead created: {monday_item_id} (score: {lead_score})"
                    )

                # Alert for high-priority leads
                if lead_score >= 70:
                    try:
                        self.email_service.send_email(
                            to_email=self.admin_email,
                            subject=f"🔥 HIGH PRIORITY LEAD - Score: {lead_score}/100",
                            html_content=f"""
                            <h2>New High-Priority Lead!</h2>
                            <p><strong>Name:</strong> {lead.name}</p>
                            <p><strong>Email:</strong> {lead.email}</p>
                            <p><strong>Score:</strong> {lead_score}</p>
                            <p><strong>Monday.com ID:</strong> {monday_item_id}</p>
                            """,
                        )
                        print(f"ALERT: High-priority lead: {lead.name}, score: {lead_score}")
                    except Exception as e:
                        print(f"Failed to send high-priority alert: {e}")

                # Clear awaiting flag
                conversation.awaiting_confirmation = False

                # Append confirmation message to bot response
                confirmation_msg = (
                    f"✅ Dziękuję za potwierdzenie! Twoje dane zostały zapisane.\n\n"
                    f"Nasz zespół skontaktuje się z Tobą wkrótce.\n\n"
                )
                context["bot_response"] = confirmation_msg + (bot_response or "")

            except Exception as e:
                print(f"[Confirmed Lead] Error: {e}")
                # Don't let lead creation failure stop the chat flow completely
                context["bot_response"] = (
                    (bot_response or "")
                    + "\nPewnie, wystąpił problem przy zapisywaniu Twoich danych. Spróbuj ponownie później."
                )

        elif confirmation_intent == "edit":
            # User wants to edit - clear awaiting flag
            conversation.awaiting_confirmation = False
            context["bot_response"] = (
                "Oczywiście! Popraw dane które chcesz zmienić, a ja je zaktualizuję. 📝"
            )

        # Fallback: Auto-create lead if enough data and no confirmation was asked/needed
        elif not conversation.awaiting_confirmation and not existing_lead:
            if has_enough_data_for_lead:
                try:
                    message_count = (
                        self.db_session.query(ChatMessage)
                        .filter_by(conversation_id=conversation.id)
                        .count()
                    )
                    lead_score = calculate_lead_score(context_memory, message_count)

                    all_messages = (
                        self.db_session.query(ChatMessage)
                        .filter_by(conversation_id=conversation.id)
                        .order_by(ChatMessage.timestamp.asc())
                        .all()
                    )
                    conv_summary = generate_conversation_summary(all_messages, context_memory)

                    lead = Lead(
                        session_id=session_id,
                        name=context_memory.get("name", "Unknown"),
                        email=context_memory.get("email"),
                        phone=context_memory.get("phone"),
                        location=context_memory.get("city"),
                        property_size=context_memory.get("square_meters"),
                        interested_package=context_memory.get("package"),
                        source="chatbot",
                        status="new",
                        lead_score=lead_score,
                        conversation_summary=conv_summary,
                        data_confirmed=False,
                        last_interaction=datetime.now(timezone.utc),
                    )

                    self.db_session.add(lead)
                    self.db_session.flush()

                    # Check for competitive mentions
                    competitor_intel = (
                        self.db_session.query(CompetitiveIntel)
                        .filter_by(session_id=session_id)
                        .order_by(CompetitiveIntel.created_at.desc())
                        .first()
                    )
                    competitor_name = competitor_intel.competitor_name if competitor_intel else None
                    next_action = suggest_next_best_action(context_memory, lead_score)

                    monday_item_id = self.monday_client.create_lead_item(
                        {
                            "name": lead.name,
                            "email": lead.email,
                            "phone": lead.phone,
                            "message": f"Lead Score: {lead_score}/100 | {conv_summary}",
                            "property_type": "Mieszkanie",  # Defaulting
                            "budget": context_memory.get("square_meters", ""),
                            "lead_score": lead_score,
                            "competitor_mentioned": competitor_name,
                            "next_action": next_action,
                        }
                    )

                    if monday_item_id:
                        lead.monday_item_id = monday_item_id
                        print(f"[Monday] Auto-lead created: {monday_item_id} (score: {lead_score})")

                except Exception as e:
                    print(f"[Auto Lead] Error: {e}")
                    # Don't let auto-lead creation failure stop the chat flow completely

        # --- Confirmation prompt (if lead not yet created) ---
        if not existing_lead:  # Only ask for confirmation if lead isn't already in DB
            should_confirm = self._should_ask_for_confirmation(context_memory, conversation)
            print(
                f"[CONFIRMATION CHECK] should_confirm={should_confirm}, context={context_memory}, awaiting={conversation.awaiting_confirmation}"
            )
            if should_confirm:
                conversation.awaiting_confirmation = True
                confirmation_msg = self._format_data_confirmation_message(context_memory)
                # Prepend confirmation message to current bot response, if any
                context["bot_response"] = (bot_response or "") + f"\n\n{confirmation_msg}"
                print("[CONFIRMATION] Added confirmation message to response")

        return context
