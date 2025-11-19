"""
Appointment Reminder Service
=============================
SMS/Email reminders for bookings via Twilio and SMTP
"""

import os
from datetime import datetime
from typing import List
from twilio.rest import Client
from src.services.email_service import EmailService

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


class AppointmentReminderService:
    """Send appointment reminders via SMS and Email"""

    def __init__(self):
        self.email_service = EmailService()

        # Initialize Twilio if configured
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            try:
                self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                self.sms_enabled = True
                print("✅ Twilio SMS enabled")
            except Exception as e:
                print(f"⚠️ Twilio unavailable: {e}")
                self.sms_enabled = False
        else:
            self.sms_enabled = False
            print("⚠️ Twilio not configured (set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)")

    def send_sms_reminder(
        self, to_phone: str, name: str, appointment_date: str, appointment_time: str
    ) -> bool:
        """
        Send SMS reminder

        Args:
            to_phone: Phone number with country code (+48...)
            name: Customer name
            appointment_date: Date string (YYYY-MM-DD)
            appointment_time: Time string (HH:MM)
        """
        if not self.sms_enabled:
            print("SMS not enabled")
            return False

        try:
            message_body = f"""
Przypomnienie NovaHouse! 🏠

Dzień dobry {name},

Przypominamy o spotkaniu:
📅 {appointment_date}
🕐 {appointment_time}

Adres: ul. Przykładowa 123, Warszawa

W razie pytań: +48 123 456 789

Do zobaczenia!
NovaHouse Team
            """.strip()

            message = self.twilio_client.messages.create(
                body=message_body, from_=TWILIO_PHONE_NUMBER, to=to_phone
            )

            print(f"✅ SMS sent to {to_phone}: {message.sid}")
            return True

        except Exception as e:
            print(f"❌ SMS send error: {e}")
            return False

    def send_email_reminder(
        self,
        to_email: str,
        name: str,
        appointment_date: str,
        appointment_time: str,
        service_type: str = "Konsultacja",
    ) -> bool:
        """Send email reminder"""
        try:
            subject = f"Przypomnienie: Spotkanie NovaHouse - {appointment_date}"

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .info-box {{ background: white; padding: 20px; margin: 20px 0; border-left: 4px solid #667eea; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 Przypomnienie o spotkaniu</h1>
        </div>
        <div class="content">
            <p>Dzień dobry <strong>{name}</strong>,</p>

            <p>Przypominamy o Twoim spotkaniu w NovaHouse:</p>

            <div class="info-box">
                <p><strong>📅 Data:</strong> {appointment_date}</p>
                <p><strong>🕐 Godzina:</strong> {appointment_time}</p>
                <p><strong>🔧 Usługa:</strong> {service_type}</p>
                <p><strong>📍 Miejsce:</strong> ul. Przykładowa 123, Warszawa</p>
            </div>

            <p><strong>Co ze sobą zabrać:</strong></p>
            <ul>
                <li>Zdjęcia pomieszczenia (jeśli masz)</li>
                <li>Pomiary (jeśli wykonane)</li>
                <li>Inspiracje (Pinterest, zdjęcia)</li>
            </ul>

            <p>W razie pytań lub potrzeby przełożenia terminu, prosimy o kontakt:</p>
            <p>📞 <strong>+48 123 456 789</strong><br>
            📧 <strong>kontakt@novahouse.pl</strong></p>

            <p>Do zobaczenia!</p>
            <p><strong>Zespół NovaHouse</strong></p>
        </div>
        <div class="footer">
            <p>© 2025 NovaHouse. Wszystkie prawa zastrzeżone.</p>
            <p>To automatyczna wiadomość przypominająca.</p>
        </div>
    </div>
</body>
</html>
            """

            return self.email_service.send_email(to_email, subject, html_body)

        except Exception as e:
            print(f"❌ Email reminder error: {e}")
            return False

    def send_reminder(
        self,
        name: str,
        email: str,
        phone: str,
        appointment_date: str,
        appointment_time: str,
        service_type: str = "Konsultacja",
        channels: List[str] = ["email", "sms"],
    ) -> dict:
        """
        Send reminder via multiple channels

        Args:
            channels: List of channels ('email', 'sms')

        Returns:
            dict with success status for each channel
        """
        results = {}

        if "email" in channels:
            results["email"] = self.send_email_reminder(
                email, name, appointment_date, appointment_time, service_type
            )

        if "sms" in channels and phone:
            results["sms"] = self.send_sms_reminder(phone, name, appointment_date, appointment_time)

        return results

    def schedule_reminder(
        self, booking_id: int, reminder_time: datetime, channels: List[str] = ["email", "sms"]
    ):
        """
        Schedule a reminder for later (used with APScheduler)

        Args:
            booking_id: Booking ID
            reminder_time: When to send reminder
            channels: Channels to use
        """
        # This will be called by APScheduler
        # Implementation depends on your booking model

    def get_upcoming_appointments(self, hours_ahead: int = 24) -> List[dict]:
        """
        Get appointments scheduled within next X hours

        Returns list of appointments that need reminders
        """
        # This depends on your booking model
        # Example:
        """
        from src.models.booking import Booking

        now = datetime.now(timezone.utc)
        future = now + timedelta(hours=hours_ahead)

        bookings = Booking.query.filter(
            and_(
                Booking.appointment_time >= now,
                Booking.appointment_time <= future,
                Booking.reminder_sent == False
            )
        ).all()

        return [booking.to_dict() for booking in bookings]
        """
        return []


# Global instance
reminder_service = AppointmentReminderService()
