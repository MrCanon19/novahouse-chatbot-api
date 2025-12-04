"""
Lead Assignment Service

Handles automatic assignment of leads to sales team.
Includes SLA tracking and notifications.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import requests

from src.models.chatbot import Lead, db


class LeadAssignmentService:
    """Service for assigning leads to sales team"""

    # Default SLA (Service Level Agreement) - 24 hours to contact lead
    SLA_HOURS = int(os.getenv("LEAD_SLA_HOURS", "24"))

    @staticmethod
    def get_available_sales_users() -> List[Dict]:
        """
        Get list of available sales users for assignment

        Returns:
            List of user dicts with {id, name, email, current_load}
        """
        # TODO: Implement actual user assignment from database
        # For now, return mock data
        return [
            {
                "id": "user_1",
                "name": "Jan Kowalski",
                "email": "jan@novahouse.pl",
                "current_load": 5,
            },
            {
                "id": "user_2",
                "name": "Maria Nowak",
                "email": "maria@novahouse.pl",
                "current_load": 3,
            },
            {
                "id": "user_3",
                "name": "Piotr Lewandowski",
                "email": "piotr@novahouse.pl",
                "current_load": 7,
            },
        ]

    @classmethod
    def assign_lead_to_user(cls, lead_id: int, user_id: str) -> tuple:
        """
        Assign a lead to specific user

        Args:
            lead_id: Lead ID
            user_id: Sales user ID

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return False, "Lead not found"

            lead.assigned_to_user_id = user_id
            lead.assigned_at = datetime.now(timezone.utc)
            lead.expected_contact_by = datetime.now(timezone.utc) + timedelta(hours=cls.SLA_HOURS)

            db.session.commit()

            # Send notification to sales user
            cls._notify_assignment(lead, user_id)

            return True, f"Lead assigned to {user_id}"

        except Exception as e:
            print(f"[Assignment] Error assigning lead: {e}")
            return False, f"Assignment failed: {str(e)}"

    @classmethod
    def auto_assign_lead(cls, lead: Lead) -> tuple:
        """
        Auto-assign lead to least busy sales user

        Args:
            lead: Lead object

        Returns:
            Tuple of (success: bool, assigned_user_id: str)
        """
        try:
            users = cls.get_available_sales_users()
            if not users:
                return False, None

            # Assign to user with lowest current load
            least_busy_user = min(users, key=lambda u: u["current_load"])

            success, message = cls.assign_lead_to_user(lead.id, least_busy_user["id"])
            if success:
                print(
                    f"[Assignment] Lead {lead.id} auto-assigned to {least_busy_user['name']} "
                    f"(load: {least_busy_user['current_load']})"
                )
            return success, least_busy_user["id"]

        except Exception as e:
            print(f"[Assignment] Error auto-assigning lead: {e}")
            return False, None

    @staticmethod
    def _notify_assignment(lead: Lead, user_id: str) -> None:
        """Send notification to assigned sales user"""
        try:
            # Get user details
            users = LeadAssignmentService.get_available_sales_users()
            user = next((u for u in users if u["id"] == user_id), None)
            if not user:
                return

            email = user["email"]
            slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

            # Send Slack notification
            if slack_webhook:
                LeadAssignmentService._send_slack_notification(lead, user, slack_webhook)

            # Send email notification
            LeadAssignmentService._send_email_notification(lead, user, email)

        except Exception as e:
            print(f"[Assignment] Error sending notification: {e}")

    @staticmethod
    def _send_slack_notification(lead: Lead, user: Dict, webhook_url: str) -> None:
        """Send Slack notification about new lead assignment"""
        try:
            payload = {
                "text": f"🆕 New Lead Assigned",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*New Lead for {user['name']}*\n\n"
                            f"👤 *{lead.name}*\n"
                            f"📧 {lead.email or 'N/A'}\n"
                            f"📱 {lead.phone or 'N/A'}\n"
                            f"📍 {lead.location or 'Unknown'}\n"
                            f"⭐ Score: {lead.lead_score}/100",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Contact by:* {lead.expected_contact_by.strftime('%Y-%m-%d %H:%M')}\n"
                            f"*Package:* {lead.interested_package or 'Not specified'}",
                        },
                    },
                ],
            }

            requests.post(webhook_url, json=payload, timeout=5)

        except Exception as e:
            print(f"[Slack] Error sending notification: {e}")

    @staticmethod
    def _send_email_notification(lead: Lead, user: Dict, email: str) -> None:
        """Send email notification about new lead assignment"""
        try:
            from src.services.email_service import email_service

            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Nowy Lead Przypisany</h2>
                <p>Cześć {user['name']}!</p>
                <p>Nowy lead został Ci przypisany:</p>

                <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                    <tr style="background-color: #f2f2f2;">
                        <td style="padding: 8px; border: 1px solid #ddd;">Imię i Nazwisko</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{lead.name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Email</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{lead.email or 'N/A'}</td>
                    </tr>
                    <tr style="background-color: #f2f2f2;">
                        <td style="padding: 8px; border: 1px solid #ddd;">Telefon</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{lead.phone or 'N/A'}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Lokalizacja</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{lead.location or 'Nieznana'}</td>
                    </tr>
                    <tr style="background-color: #f2f2f2;">
                        <td style="padding: 8px; border: 1px solid #ddd;">Paczka</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{lead.interested_package or 'Nieokreślona'}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Wynik</td>
                        <td style="padding: 8px; border: 1px solid #ddd;"><strong>{lead.lead_score}/100</strong></td>
                    </tr>
                    <tr style="background-color: #f2f2f2;">
                        <td style="padding: 8px; border: 1px solid #ddd;">Kontakt do</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{lead.expected_contact_by.strftime('%Y-%m-%d %H:%M')}</td>
                    </tr>
                </table>

                <p>Pamiętaj o kontakcie w ciągu {LeadAssignmentService.SLA_HOURS} godzin!</p>
                <p>Pozdrawiamy,<br>Zespół NovaHouse</p>
            </body>
            </html>
            """

            email_service.send_email(
                to=email,
                subject=f"NovaHouse - Nowy Lead: {lead.name}",
                html=html_body,
            )

        except Exception as e:
            print(f"[Email] Error sending notification: {e}")

    @staticmethod
    def check_sla_breach(lead: Lead) -> bool:
        """
        Check if lead SLA has been breached

        Args:
            lead: Lead object

        Returns:
            True if SLA breached (expected_contact_by < now)
        """
        if not lead.expected_contact_by:
            return False

        return datetime.now(timezone.utc) > lead.expected_contact_by

    @staticmethod
    def get_sla_status(lead: Lead) -> Dict:
        """
        Get SLA status for lead

        Args:
            lead: Lead object

        Returns:
            Dict with status info
        """
        if not lead.assigned_at:
            return {"status": "not_assigned", "hours_remaining": None}

        expected = lead.expected_contact_by
        now = datetime.now(timezone.utc)

        if now > expected:
            return {
                "status": "breached",
                "hours_remaining": 0,
                "breached_by": (now - expected).total_seconds() / 3600,
            }
        else:
            hours_remaining = (expected - now).total_seconds() / 3600
            return {
                "status": "active",
                "hours_remaining": round(hours_remaining, 1),
            }


# Singleton instance
lead_assignment_service = LeadAssignmentService()
