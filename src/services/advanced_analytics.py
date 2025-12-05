"""
Advanced Analytics Service

Conversion funnel analysis, weekly trends, intent distribution.
Helps understand user behavior and optimize conversion rates.
"""

import csv
import io
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Dict

from src.models.chatbot import ChatConversation, ChatMessage, Lead, db


class AdvancedAnalyticsService:
    """Service for advanced analytics and reporting"""

    @staticmethod
    def get_conversion_funnel() -> Dict:
        """
        Analyze conversion funnel - where users drop off

        Returns:
            Dict with funnel stages and conversion rates
        """
        try:
            # Total conversations started
            total_conversations = ChatConversation.query.count()

            # Conversations with at least one message
            conversations_with_messages = (
                db.session.query(ChatConversation.id).join(ChatMessage).distinct().count()
            )

            # Conversations with name collected
            conversations_with_name = ChatConversation.query.filter(
                ChatConversation.context_data.like('%"name":%')
            ).count()

            # Conversations with contact (email or phone)
            conversations_with_contact = ChatConversation.query.filter(
                db.or_(
                    ChatConversation.context_data.like('%"email":%'),
                    ChatConversation.context_data.like('%"phone":%'),
                )
            ).count()

            # Leads created (converted)
            total_leads = Lead.query.count()

            # Verified leads (email or phone verified)
            verified_leads = Lead.query.filter(
                db.or_(Lead.email_verified.is_(True), Lead.phone_verified.is_(True))
            ).count()

            # Calculate conversion rates
            def safe_rate(numerator, denominator):
                return round((numerator / denominator) * 100, 2) if denominator > 0 else 0

            return {
                "funnel": [
                    {
                        "stage": "Rozmowa rozpoczęta",
                        "count": total_conversations,
                        "rate": 100.0,
                        "description": "Użytkownicy, którzy rozpoczęli rozmowę",
                    },
                    {
                        "stage": "Pierwsze pytanie",
                        "count": conversations_with_messages,
                        "rate": safe_rate(conversations_with_messages, total_conversations),
                        "description": "Użytkownicy, którzy wysłali wiadomość",
                    },
                    {
                        "stage": "Podali imię",
                        "count": conversations_with_name,
                        "rate": safe_rate(conversations_with_name, total_conversations),
                        "description": "Użytkownicy, którzy podali imię",
                    },
                    {
                        "stage": "Podali kontakt",
                        "count": conversations_with_contact,
                        "rate": safe_rate(conversations_with_contact, total_conversations),
                        "description": "Użytkownicy z email lub telefon",
                    },
                    {
                        "stage": "Lead utworzony",
                        "count": total_leads,
                        "rate": safe_rate(total_leads, total_conversations),
                        "description": "Leady utworzone w systemie",
                    },
                    {
                        "stage": "Lead zweryfikowany",
                        "count": verified_leads,
                        "rate": safe_rate(verified_leads, total_conversations),
                        "description": "Leady z potwierdzonym kontaktem",
                    },
                ],
                "overall_conversion_rate": safe_rate(total_leads, total_conversations),
                "verification_rate": safe_rate(verified_leads, total_leads),
                "drop_off_points": AdvancedAnalyticsService._identify_drop_offs(
                    total_conversations,
                    conversations_with_messages,
                    conversations_with_name,
                    conversations_with_contact,
                    total_leads,
                ),
            }

        except Exception as e:
            print(f"[Analytics] Error in conversion funnel: {e}")
            return {"error": str(e)}

    @staticmethod
    def _identify_drop_offs(conv_total, conv_msg, conv_name, conv_contact, leads):
        """Identify biggest drop-off points in funnel"""
        drop_offs = []

        if conv_total > 0:
            msg_drop = ((conv_total - conv_msg) / conv_total) * 100
            if msg_drop > 20:
                drop_offs.append(
                    {
                        "stage": "Rozmowa → Pierwsze pytanie",
                        "drop_rate": round(msg_drop, 2),
                        "severity": "high" if msg_drop > 40 else "medium",
                    }
                )

            if conv_msg > 0:
                name_drop = ((conv_msg - conv_name) / conv_msg) * 100
                if name_drop > 20:
                    drop_offs.append(
                        {
                            "stage": "Pierwsze pytanie → Podanie imienia",
                            "drop_rate": round(name_drop, 2),
                            "severity": "high" if name_drop > 40 else "medium",
                        }
                    )

            if conv_name > 0:
                contact_drop = ((conv_name - conv_contact) / conv_name) * 100
                if contact_drop > 20:
                    drop_offs.append(
                        {
                            "stage": "Imię → Kontakt",
                            "drop_rate": round(contact_drop, 2),
                            "severity": "high" if contact_drop > 40 else "medium",
                        }
                    )

        return drop_offs

    @staticmethod
    def get_weekly_trends(weeks: int = 4) -> Dict:
        """
        Get weekly trends for leads, conversations, and conversions

        Args:
            weeks: Number of weeks to analyze (default 4)

        Returns:
            Dict with weekly statistics
        """
        try:
            now = datetime.now(timezone.utc)
            start_date = now - timedelta(weeks=weeks)

            trends = []

            for week_num in range(weeks):
                week_start = start_date + timedelta(weeks=week_num)
                week_end = week_start + timedelta(weeks=1)

                # Count conversations for this week
                conversations_count = ChatConversation.query.filter(
                    ChatConversation.started_at >= week_start,
                    ChatConversation.started_at < week_end,
                ).count()

                # Count leads for this week
                leads_count = Lead.query.filter(
                    Lead.created_at >= week_start, Lead.created_at < week_end
                ).count()

                # Count high-score leads
                high_score_leads = Lead.query.filter(
                    Lead.created_at >= week_start,
                    Lead.created_at < week_end,
                    Lead.lead_score >= 70,
                ).count()

                # Calculate conversion rate
                conversion_rate = (
                    round((leads_count / conversations_count) * 100, 2)
                    if conversations_count > 0
                    else 0
                )

                trends.append(
                    {
                        "week": f"Week {week_num + 1}",
                        "start_date": week_start.strftime("%Y-%m-%d"),
                        "end_date": week_end.strftime("%Y-%m-%d"),
                        "conversations": conversations_count,
                        "leads": leads_count,
                        "high_score_leads": high_score_leads,
                        "conversion_rate": conversion_rate,
                    }
                )

            # Calculate overall statistics
            total_conversations = sum(t["conversations"] for t in trends)
            total_leads = sum(t["leads"] for t in trends)
            avg_conversion = (
                round((total_leads / total_conversations) * 100, 2)
                if total_conversations > 0
                else 0
            )

            return {
                "period": f"Last {weeks} weeks",
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": now.strftime("%Y-%m-%d"),
                "weekly_data": trends,
                "totals": {
                    "conversations": total_conversations,
                    "leads": total_leads,
                    "avg_conversion_rate": avg_conversion,
                },
            }

        except Exception as e:
            print(f"[Analytics] Error in weekly trends: {e}")
            return {"error": str(e)}

    @staticmethod
    def get_intent_distribution() -> Dict:
        """
        Analyze what users are asking about (intent distribution)

        Returns:
            Dict with intent counts and percentages
        """
        try:
            # Get all user messages
            messages = (
                ChatMessage.query.filter(ChatMessage.sender == "user")
                .order_by(ChatMessage.timestamp.desc())
                .limit(1000)  # Last 1000 messages
                .all()
            )

            # Categorize intents based on keywords
            intent_keywords = {
                "pricing": ["cena", "koszt", "ile kosztuje", "cennik", "zł"],
                "packages": ["pakiet", "standard", "premium", "express", "basic"],
                "timeframe": ["kiedy", "jak długo", "termin", "czas"],
                "process": ["jak", "proces", "etap", "krok"],
                "booking": [
                    "spotkanie",
                    "konsultacja",
                    "umówić",
                    "rezerwacja",
                    "wizyta",
                ],
                "location": ["miasto", "gdzie", "lokalizacja", "obszar"],
                "contact": ["kontakt", "telefon", "email", "numer"],
                "materials": ["materiały", "katalog", "wybór", "produkty"],
            }

            intent_counts = Counter()
            total_messages = len(messages)

            for msg in messages:
                message_lower = msg.message.lower()
                matched = False

                for intent, keywords in intent_keywords.items():
                    if any(keyword in message_lower for keyword in keywords):
                        intent_counts[intent] += 1
                        matched = True

                if not matched:
                    intent_counts["other"] += 1

            # Calculate percentages
            intent_distribution = []
            for intent, count in intent_counts.most_common():
                percentage = round((count / total_messages) * 100, 2)
                intent_distribution.append(
                    {"intent": intent, "count": count, "percentage": percentage}
                )

            return {
                "total_messages_analyzed": total_messages,
                "intent_distribution": intent_distribution,
                "top_intent": (intent_counts.most_common(1)[0][0] if intent_counts else "unknown"),
            }

        except Exception as e:
            print(f"[Analytics] Error in intent distribution: {e}")
            return {"error": str(e)}

    @staticmethod
    def export_to_csv(data_type: str, filters: Dict = None) -> str:
        """
        Export data to CSV format

        Args:
            data_type: Type of data to export ("leads", "conversations", "funnel")
            filters: Optional filters (date range, status, etc.)

        Returns:
            CSV string
        """
        try:
            output = io.StringIO()

            if data_type == "leads":
                writer = csv.writer(output)
                writer.writerow(
                    [
                        "ID",
                        "Name",
                        "Email",
                        "Phone",
                        "City",
                        "Package",
                        "Score",
                        "Status",
                        "Created",
                        "Verified",
                    ]
                )

                query = Lead.query
                if filters:
                    if filters.get("status"):
                        query = query.filter_by(status=filters["status"])
                    if filters.get("min_score"):
                        query = query.filter(Lead.lead_score >= filters["min_score"])

                leads = query.order_by(Lead.created_at.desc()).all()

                for lead in leads:
                    writer.writerow(
                        [
                            lead.id,
                            lead.name,
                            lead.email or "",
                            lead.phone or "",
                            lead.location or "",
                            lead.interested_package or "",
                            lead.lead_score,
                            lead.status,
                            lead.created_at.strftime("%Y-%m-%d %H:%M") if lead.created_at else "",
                            "Yes" if (lead.email_verified or lead.phone_verified) else "No",
                        ]
                    )

            elif data_type == "funnel":
                funnel_data = AdvancedAnalyticsService.get_conversion_funnel()
                writer = csv.writer(output)
                writer.writerow(["Stage", "Count", "Conversion Rate %", "Description"])

                for stage in funnel_data.get("funnel", []):
                    writer.writerow(
                        [
                            stage["stage"],
                            stage["count"],
                            stage["rate"],
                            stage["description"],
                        ]
                    )

            return output.getvalue()

        except Exception as e:
            print(f"[Analytics] Error exporting CSV: {e}")
            return f"Error: {str(e)}"


# Singleton instance
advanced_analytics = AdvancedAnalyticsService()
