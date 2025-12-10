"""
Context Summarization Service
Generates concise conversation summaries for Monday.com and lead records
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ContextMemory:
    """
    Typed container for conversation context data.

    Provides type safety and IDE autocomplete for context attributes.
    Use this instead of raw Dict for better maintainability.
    """

    # Personal info
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    # Property details
    city: Optional[str] = None
    square_meters: Optional[int] = None
    rooms: Optional[int] = None
    property_type: Optional[str] = None  # "mieszkanie", "dom"

    # Requirements
    package: Optional[str] = None  # Express, Comfort, Premium, etc.
    budget: Optional[int] = None
    timeline: Optional[str] = None  # "pilne", "do 3 miesięcy", "planowanie"

    # Booking
    booking_intent: bool = False
    preferred_contact: Optional[str] = None  # "email", "phone", "whatsapp"

    # RODO
    rodo_consent: bool = False
    marketing_consent: bool = False

    def to_dict(self) -> Dict:
        """Convert to dictionary for legacy compatibility"""
        from dataclasses import asdict

        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "ContextMemory":
        """Create from dictionary with safe defaults"""
        return cls(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            city=data.get("city"),
            square_meters=data.get("square_meters"),
            rooms=data.get("rooms"),
            property_type=data.get("property_type"),
            package=data.get("package"),
            budget=data.get("budget"),
            timeline=data.get("timeline"),
            booking_intent=data.get("booking_intent", False),
            preferred_contact=data.get("preferred_contact"),
            rodo_consent=data.get("rodo_consent", False),
            marketing_consent=data.get("marketing_consent", False),
        )


class ContextSummarizationService:
    """Generate smart conversation summaries"""

    def generate_summary(
        self,
        context_memory: ContextMemory | Dict,
        message_history: List[Dict],
        conversation_duration_minutes: float = 0,
    ) -> str:
        """
        Generate one-sentence conversation summary

        Args:
            context_memory: Collected context data (ContextMemory or Dict for legacy)
            message_history: List of messages with 'sender' and 'message' keys
            conversation_duration_minutes: Duration of conversation

        Returns:
            Concise summary string
        """
        # Convert to dict if ContextMemory for unified access
        if isinstance(context_memory, ContextMemory):
            ctx = context_memory.to_dict()
        else:
            ctx = context_memory

        parts = []

        # 1. Location
        city = ctx.get("city")
        if city:
            parts.append(f"Klient z {city}")
        else:
            parts.append("Klient")

        # 2. Property size
        sqm = ctx.get("square_meters")
        if sqm:
            parts.append(f"mieszkanie {sqm}m²")

        # 3. Package interest
        package = ctx.get("package")
        if package:
            parts.append(f"interesuje pakiet {package}")

        # 4. Main topics/questions
        topics = self._extract_main_topics(message_history)
        if topics:
            parts.append(f"pytania o {', '.join(topics[:2])}")  # Max 2 topics

        # 5. Urgency/timeline
        timeline = self._detect_timeline_urgency(message_history)
        if timeline:
            parts.append(timeline)

        # 6. Contact preference
        contact = self._get_contact_preference(ctx)
        if contact:
            parts.append(contact)

        # Join with proper punctuation
        if not parts:
            return "Nowa konwersacja - brak szczegółów"

        summary = parts[0]
        if len(parts) > 1:
            summary += ", " + ", ".join(parts[1:])

        summary += "."

        # Add engagement indicator
        if len(message_history) >= 10:
            summary += " ✅ Wysoko zaangażowany"
        elif conversation_duration_minutes > 5:
            summary += " ✓ Zaangażowany"

        return summary

    def _extract_main_topics(self, message_history: List[Dict]) -> List[str]:
        """Extract main topics from conversation"""
        topics = set()

        # Keywords for different topics
        topic_keywords = {
            "ceny": ["cena", "koszt", "ile", "płacę", "budżet", "price"],
            "materiały": ["materiał", "płytki", "panele", "farba", "wykończenie", "materials"],
            "czas realizacji": ["jak długo", "kiedy", "termin", "czas", "duration", "timeline"],
            "proces": ["proces", "jak przebiega", "etapy", "fazy", "process"],
            "gwarancja": ["gwarancja", "warranty", "reklamacja"],
            "doświadczenie": ["realizacje", "portfolio", "doświadczenie", "projekty"],
            "umówienie": ["spotkanie", "konsultacja", "prezentacja", "meeting"],
        }

        # Check user messages
        user_messages = [
            msg["message"].lower() for msg in message_history if msg.get("sender") == "user"
        ]
        all_text = " ".join(user_messages)

        for topic, keywords in topic_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                topics.add(topic)

        return list(topics)

    def _detect_timeline_urgency(self, message_history: List[Dict]) -> Optional[str]:
        """Detect if client has urgency/timeline"""
        user_messages = [
            msg["message"].lower() for msg in message_history if msg.get("sender") == "user"
        ]
        all_text = " ".join(user_messages)

        urgent_keywords = {
            "szybko": "pilne",
            "jak najszybciej": "bardzo pilne",
            "asap": "bardzo pilne",
            "od zaraz": "natychmiastowe",
            "w tym tygodniu": "pilne (tydzień)",
            "w tym miesiącu": "termin: miesiąc",
            "za 2 tygodnie": "termin: 2 tygodnie",
            "niedługo": "pilne",
        }

        for keyword, label in urgent_keywords.items():
            if keyword in all_text:
                return label

        return None

    def _get_contact_preference(self, context_memory: Dict) -> Optional[str]:
        """Get contact preference"""
        has_email = bool(context_memory.get("email"))
        has_phone = bool(context_memory.get("phone"))

        if has_email and has_phone:
            return "kontakt: email + telefon"
        elif has_email:
            return "kontakt: email"
        elif has_phone:
            return "kontakt: telefon"

        return None

    def generate_monday_description(
        self, context_memory: Dict, message_history: List[Dict], lead_score: int = 0
    ) -> str:
        """
        Generate detailed description for Monday.com

        Returns:
            Multi-line description with all details
        """
        lines = []

        # Header
        name = context_memory.get("name", "Nowy lead")
        lines.append(f"🙋 {name}")
        lines.append("")

        # Property details
        if context_memory.get("city") or context_memory.get("square_meters"):
            lines.append("📍 Nieruchomość:")
            if context_memory.get("city"):
                lines.append(f"   • Miasto: {context_memory['city']}")
            if context_memory.get("square_meters"):
                lines.append(f"   • Metraż: {context_memory['square_meters']}m²")
            if context_memory.get("package"):
                lines.append(f"   • Pakiet: {context_memory['package']}")
            lines.append("")

        # Contact
        lines.append("📞 Kontakt:")
        if context_memory.get("email"):
            lines.append(f"   • Email: {context_memory['email']}")
        if context_memory.get("phone"):
            lines.append(f"   • Tel: {context_memory['phone']}")
        lines.append("")

        # Topics discussed
        topics = self._extract_main_topics(message_history)
        if topics:
            lines.append("💬 Tematy rozmowy:")
            for topic in topics:
                lines.append(f"   • {topic}")
            lines.append("")

        # Lead quality
        quality = (
            "🔥 WYSOKA" if lead_score >= 70 else "⚠️ ŚREDNIA" if lead_score >= 40 else "❄️ NISKA"
        )
        lines.append(f"⭐ Jakość leada: {quality} ({lead_score}/100)")

        # Urgency
        timeline = self._detect_timeline_urgency(message_history)
        if timeline:
            lines.append(f"⏰ Priorytet: {timeline}")

        return "\n".join(lines)

    def generate_short_summary(self, context_memory: Dict) -> str:
        """
        Generate ultra-short summary for notifications

        Returns:
            One-line summary (max 60 chars)
        """
        parts = []

        if context_memory.get("city"):
            parts.append(context_memory["city"])

        if context_memory.get("square_meters"):
            parts.append(f"{context_memory['square_meters']}m²")

        if context_memory.get("package"):
            pkg = context_memory["package"]
            if "srebrny" in pkg.lower() or "silver" in pkg.lower():
                parts.append("🥈")
            elif "złoty" in pkg.lower() or "gold" in pkg.lower():
                parts.append("🥇")
            elif "platynowy" in pkg.lower() or "platinum" in pkg.lower():
                parts.append("💎")

        if not parts:
            return "Nowy lead"

        return " • ".join(parts)


# Global instance
summarization_service = ContextSummarizationService()
