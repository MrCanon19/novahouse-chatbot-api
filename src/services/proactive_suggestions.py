"""
Proactive Suggestions Service
Generates smart next-step suggestions based on conversation state
"""

from typing import Dict, List, Optional

from src.services.conversation_state_machine import ConversationState


class ProactiveSuggestionsService:
    """Generates proactive suggestions to guide conversation"""

    def get_suggestions(
        self, current_state: ConversationState, context_memory: Dict, last_user_message: str = ""
    ) -> Optional[Dict]:
        """
        Get proactive suggestions based on current state

        Returns:
            dict with suggestions or None if not applicable
        """
        if current_state == ConversationState.GREETING:
            return self._greeting_suggestions()

        elif current_state == ConversationState.COLLECTING_INFO:
            return self._collecting_info_suggestions(context_memory)

        elif current_state == ConversationState.QUALIFYING:
            return self._qualifying_suggestions(context_memory)

        elif current_state == ConversationState.CONFIRMING:
            return self._confirming_suggestions(context_memory)

        return None

    def _greeting_suggestions(self) -> Dict:
        """Suggestions for greeting state"""
        return {
            "type": "quick_actions",
            "message": "👋 Jak mogę Ci pomóc?",
            "actions": [
                {
                    "text": "💰 Wycena wykończenia",
                    "payload": "pricing_inquiry",
                    "description": "Dowiedz się ile kosztuje wykończenie",
                },
                {
                    "text": "📦 Poznaj pakiety",
                    "payload": "explore_packages",
                    "description": "Srebrny, Złoty, Platynowy",
                },
                {
                    "text": "🏠 Zobacz realizacje",
                    "payload": "view_portfolio",
                    "description": "Nasze ukończone projekty",
                },
                {
                    "text": "📅 Umów spotkanie",
                    "payload": "book_meeting",
                    "description": "Bezpłatna konsultacja",
                },
            ],
        }

    def _collecting_info_suggestions(self, context: Dict) -> Dict:
        """Suggestions while collecting info"""
        missing = self._get_missing_info(context)

        if not missing:
            return None

        # Priority order for collection
        if "city" in missing:
            return {
                "type": "info_request",
                "message": "📍 W jakim mieście jest mieszkanie?",
                "actions": [
                    {"text": "🏙️ Warszawa", "payload": "city_warszawa"},
                    {"text": "🌆 Kraków", "payload": "city_krakow"},
                    {"text": "🏛️ Wrocław", "payload": "city_wroclaw"},
                    {"text": "🌃 Inne miasto", "payload": "city_other"},
                ],
            }

        if "square_meters" in missing:
            return {
                "type": "info_request",
                "message": "📐 Ile ma metrów kwadratowych?",
                "actions": [
                    {"text": "🏡 30-50 m²", "payload": "sqm_30_50"},
                    {"text": "🏠 50-70 m²", "payload": "sqm_50_70"},
                    {"text": "🏢 70-100 m²", "payload": "sqm_70_100"},
                    {"text": "🏰 100+ m²", "payload": "sqm_100_plus"},
                ],
            }

        if "package" in missing:
            return {
                "type": "package_selection",
                "message": "💎 Który pakiet Cię interesuje?",
                "actions": [
                    {
                        "text": "🥈 Srebrny (2000 zł/m²)",
                        "payload": "package_silver",
                        "description": "Standard wykończenia",
                    },
                    {
                        "text": "🥇 Złoty (3500 zł/m²)",
                        "payload": "package_gold",
                        "description": "Premium wykończenie",
                    },
                    {
                        "text": "💎 Platynowy (5000 zł/m²)",
                        "payload": "package_platinum",
                        "description": "Luksus i design",
                    },
                ],
            }

        if "email" in missing:
            return {
                "type": "contact_request",
                "message": "📧 Podaj email aby otrzymać szczegółową wycenę",
                "actions": None,  # Text input expected
            }

        return None

    def _qualifying_suggestions(self, context: Dict) -> Dict:
        """Suggestions during qualification"""
        has_package = context.get("package") is not None
        has_sqm = context.get("square_meters") is not None

        if has_package and has_sqm:
            # Calculate approximate price
            sqm = context["square_meters"]
            package = context["package"].lower()

            price_per_sqm = {
                "srebrny": 2000,
                "silver": 2000,
                "złoty": 3500,
                "gold": 3500,
                "platynowy": 5000,
                "platinum": 5000,
            }

            price = price_per_sqm.get(package, 3000) * sqm

            return {
                "type": "qualification",
                "message": f"💰 Szacunkowy koszt: {price:,.0f} zł",
                "actions": [
                    {"text": "📋 Prześlij szczegółową wycenę", "payload": "send_detailed_quote"},
                    {"text": "📅 Umów darmową konsultację", "payload": "book_consultation"},
                    {"text": "🔄 Zmień pakiet", "payload": "change_package"},
                    {"text": "❓ Mam pytania", "payload": "ask_questions"},
                ],
            }

        return {
            "type": "next_steps",
            "message": "Co chcesz zrobić dalej?",
            "actions": [
                {"text": "💬 Porozmawiaj z doradcą", "payload": "talk_to_advisor"},
                {"text": "📱 Zostaw kontakt", "payload": "leave_contact"},
                {"text": "🏠 Zobacz realizacje", "payload": "view_portfolio"},
            ],
        }

    def _confirming_suggestions(self, context: Dict) -> Dict:
        """Suggestions during confirmation"""
        return {
            "type": "confirmation",
            "message": "✅ Czy dane są poprawne?",
            "actions": [
                {"text": "✅ Tak, potwierdź", "payload": "confirm_data"},
                {"text": "✏️ Zmień dane", "payload": "edit_data"},
                {"text": "❌ Anuluj", "payload": "cancel"},
            ],
        }

    def _get_missing_info(self, context: Dict) -> List[str]:
        """Get list of missing information"""
        required = ["city", "square_meters", "package", "email"]
        return [field for field in required if not context.get(field)]

    def get_smart_clarification(self, unclear_input: str, context: Dict) -> Dict:
        """Generate clarification question for unclear input"""
        unclear_lower = unclear_input.lower()

        # Check if asking about packages first
        if any(word in unclear_lower for word in ["pakiet", "express", "comfort", "premium", "indywidualny"]):
            return {
                "type": "clarification",
                "message": "📦 Pytasz o pakiety wykończeniowe? Mogę powiedzieć o:",
                "actions": [
                    {"text": "Express (999 zł/m²)", "payload": "pkg_express"},
                    {"text": "Express Plus (1199 zł/m²)", "payload": "pkg_express_plus"},
                    {"text": "Comfort (1499 zł/m²)", "payload": "pkg_comfort"},
                    {"text": "Premium (1999 zł/m²)", "payload": "pkg_premium"},
                    {"text": "Porównanie pakietów", "payload": "pkg_compare"},
                ],
            }

        # Check what they might be asking about
        if any(word in unclear_lower for word in ["cena", "koszt", "ile", "płacę", "price"]):
            return {
                "type": "clarification",
                "message": "💰 Pytasz o cenę? Mogę podać cenę:",
                "actions": [
                    {"text": "Pakietów wykończenia", "payload": "price_packages"},
                    {"text": "Konkretnej usługi", "payload": "price_service"},
                    {"text": "Materiałów", "payload": "price_materials"},
                    {"text": "Wycenę mojego mieszkania", "payload": "price_my_apartment"},
                ],
            }

        if any(word in unclear_lower for word in ["czas", "jak długo", "kiedy", "termin", "time"]):
            return {
                "type": "clarification",
                "message": "⏰ Pytasz o czas? Chcesz wiedzieć:",
                "actions": [
                    {"text": "Jak długo trwa wykończenie", "payload": "duration_finishing"},
                    {"text": "Kiedy można zacząć", "payload": "start_date"},
                    {"text": "Terminy płatności", "payload": "payment_schedule"},
                ],
            }

        if any(word in unclear_lower for word in ["gdzie", "region", "miasto", "where"]):
            return {
                "type": "clarification",
                "message": "📍 Pytasz o lokalizację?",
                "actions": [
                    {"text": "Gdzie działamy", "payload": "coverage_areas"},
                    {"text": "Gdzie są wasze biura", "payload": "office_locations"},
                    {"text": "Moje miasto to...", "payload": "specify_city"},
                ],
            }

        # Generic clarification
        return {
            "type": "clarification",
            "message": "🤔 Nie jestem pewien co masz na myśli. Możesz zapytać o:",
            "actions": [
                {"text": "💰 Ceny i pakiety", "payload": "ask_pricing"},
                {"text": "⏱️ Czas realizacji", "payload": "ask_timeline"},
                {"text": "📋 Proces wykończenia", "payload": "ask_process"},
                {"text": "🏠 Nasze realizacje", "payload": "ask_portfolio"},
            ],
        }


# Global instance
proactive_suggestions = ProactiveSuggestionsService()
