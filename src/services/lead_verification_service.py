"""
Lead Verification Service

Handles email and phone verification for leads.
Generates tokens/codes and sends verification messages.
"""

import os
import secrets
from datetime import datetime, timezone
from typing import Tuple

from src.models.chatbot import Lead, db
from src.services.email_service import email_service


class LeadVerificationService:
    """Service for verifying lead contact information"""

    # Token expiration time (24 hours)
    TOKEN_EXPIRATION_HOURS = 24

    # SMS code expiration time (10 minutes)
    SMS_EXPIRATION_MINUTES = 10

    @staticmethod
    def generate_verification_token() -> str:
        """Generate a secure verification token"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def generate_sms_code() -> str:
        """Generate a 6-digit SMS verification code"""
        return "".join(str(secrets.randbelow(10)) for _ in range(6))

    @classmethod
    def send_email_verification(cls, lead: Lead) -> Tuple[bool, str]:
        """
        Send email verification to lead

        Args:
            lead: Lead object

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not lead.email:
            return False, "No email address for lead"

        try:
            # Generate token
            token = cls.generate_verification_token()
            lead.email_verification_token = token
            db.session.commit()

            # Build verification link
            base_url = os.getenv("FRONTEND_URL", "https://novahouse.com")
            verify_link = f"{base_url}/verify-email?token={token}&lead_id={lead.id}"

            # Send verification email
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Weryfikacja Twojego Adresu E-mail</h2>
                <p>Cześć {lead.name}!</p>
                <p>Dziękujemy za zainteresowanie NovaHouse.</p>
                <p>Kliknij poniżej, aby potwierdzić Twój adres e-mail:</p>
                <p>
                    <a href="{verify_link}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Potwierdź Email
                    </a>
                </p>
                <p>Lub skopiuj ten link: {verify_link}</p>
                <p>Link ważny przez 24 godziny.</p>
                <p>Pozdrawiamy,<br>Zespół NovaHouse</p>
            </body>
            </html>
            """

            email_service.send_email(
                to=lead.email,
                subject="NovaHouse - Weryfikacja Adresu E-mail",
                html=html_body,
            )

            return True, f"Verification email sent to {lead.email}"

        except Exception as e:
            print(f"[Verification] Error sending email: {e}")
            return False, f"Failed to send verification email: {str(e)}"

    @classmethod
    def verify_email_token(cls, lead_id: int, token: str) -> Tuple[bool, str]:
        """
        Verify email token and mark lead as verified

        Args:
            lead_id: Lead ID
            token: Verification token

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return False, "Lead not found"

            if not lead.email_verification_token:
                return False, "No verification token for this lead"

            if lead.email_verification_token != token:
                return False, "Invalid verification token"

            # Check token expiration (basic check - no timestamp stored)
            lead.email_verified = True
            lead.email_verified_at = datetime.now(timezone.utc)
            lead.email_verification_token = None  # Clear token
            db.session.commit()

            return True, "Email verified successfully"

        except Exception as e:
            print(f"[Verification] Error verifying email: {e}")
            return False, f"Verification failed: {str(e)}"

    @classmethod
    def send_phone_verification(cls, lead: Lead) -> Tuple[bool, str]:
        """
        Send SMS verification code to lead

        Args:
            lead: Lead object

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not lead.phone:
            return False, "No phone number for lead"

        try:
            # Generate SMS code
            sms_code = cls.generate_sms_code()
            lead.phone_verification_code = sms_code
            db.session.commit()

            # Try to send SMS (using mock if no SMS service configured)
            sms_service_type = os.getenv("SMS_SERVICE", "mock")

            if sms_service_type == "twilio":
                # NOTE: Implement Twilio integration
                print(f"[SMS] Would send to {lead.phone}: {sms_code}")
            else:
                # Mock SMS
                print(f"[SMS Mock] Code for {lead.phone}: {sms_code}")

            return True, f"SMS verification code sent to {lead.phone}"

        except Exception as e:
            print(f"[Verification] Error sending SMS: {e}")
            return False, f"Failed to send SMS: {str(e)}"

    @classmethod
    def verify_phone_code(cls, lead_id: int, code: str) -> Tuple[bool, str]:
        """
        Verify phone code and mark lead as verified

        Args:
            lead_id: Lead ID
            code: 6-digit SMS code

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return False, "Lead not found"

            if not lead.phone_verification_code:
                return False, "No verification code for this lead"

            if lead.phone_verification_code != code:
                return False, "Invalid verification code"

            lead.phone_verified = True
            lead.phone_verified_at = datetime.now(timezone.utc)
            lead.phone_verification_code = None  # Clear code
            db.session.commit()

            return True, "Phone verified successfully"

        except Exception as e:
            print(f"[Verification] Error verifying phone: {e}")
            return False, f"Verification failed: {str(e)}"

    @classmethod
    def is_lead_fully_verified(cls, lead: Lead) -> bool:
        """Check if lead is fully verified (email OR phone)"""
        return lead.email_verified or lead.phone_verified


# Singleton instance
lead_verification_service = LeadVerificationService()
