"""
Email Notification Service
Wysyłanie emaili dla leadów, rezerwacji i raportów
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional, Dict, Any


class EmailService:
    """Service do wysyłania emaili"""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_user)
        self.admin_email = os.getenv("ADMIN_EMAIL", "kontakt@novahouse.pl")
        self.enabled = bool(self.smtp_user and self.smtp_password)

    def send_email(
        self, to_email: str, subject: str, html_content: str, text_content: Optional[str] = None
    ) -> bool:
        """Wysyła email"""
        if not self.enabled:
            print(f"Email disabled - would send to {to_email}: {subject}")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email

            # Text version (fallback)
            if text_content:
                part1 = MIMEText(text_content, "plain", "utf-8")
                msg.attach(part1)

            # HTML version
            part2 = MIMEText(html_content, "html", "utf-8")
            msg.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            print(f"✅ Email sent to {to_email}: {subject}")
            return True

        except Exception as e:
            print(f"❌ Email error: {e}")
            return False

    def send_new_lead_notification(self, lead_data: Dict[str, Any]) -> bool:
        """Wysyła notyfikację o nowym leadzie do admina"""
        subject = f"🎯 Nowy Lead: {lead_data.get('name', 'Nieznany')}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .field {{ margin: 15px 0; padding: 10px; background: #f9fafb; border-left: 4px solid #667eea; }}
                .label {{ font-weight: bold; color: #667eea; }}
                .value {{ margin-top: 5px; color: #333; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">🎯 Nowy Lead w NovaHouse!</h2>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">
                        {datetime.now().strftime('%d.%m.%Y %H:%M')}
                    </p>
                </div>

                <div class="field">
                    <div class="label">Imię i Nazwisko:</div>
                    <div class="value">{lead_data.get('name', 'Brak')}</div>
                </div>

                <div class="field">
                    <div class="label">Email:</div>
                    <div class="value">{lead_data.get('email', 'Brak')}</div>
                </div>

                <div class="field">
                    <div class="label">Telefon:</div>
                    <div class="value">{lead_data.get('phone', 'Brak')}</div>
                </div>

                <div class="field">
                    <div class="label">Wiadomość:</div>
                    <div class="value">{lead_data.get('message', 'Brak')}</div>
                </div>

                <div class="field">
                    <div class="label">Status:</div>
                    <div class="value">{lead_data.get('status', 'new')}</div>
                </div>

                {f'''
                <div class="field">
                    <div class="label">Pakiet:</div>
                    <div class="value">{lead_data.get('package')}</div>
                </div>
                ''' if lead_data.get('package') else ''}

                {f'''
                <div class="field">
                    <div class="label">Budżet:</div>
                    <div class="value">{lead_data.get('budget')}</div>
                </div>
                ''' if lead_data.get('budget') else ''}

                <div class="footer">
                    <p>Zaloguj się do panelu admina aby odpowiedzieć na zapytanie:</p>
                    <p><a href="https://glass-core-467907-e9.ey.r.appspot.com/admin" style="color: #667eea;">
                        👉 Panel Admina
                    </a></p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Nowy Lead w NovaHouse!

        Imię: {lead_data.get('name', 'Brak')}
        Email: {lead_data.get('email', 'Brak')}
        Telefon: {lead_data.get('phone', 'Brak')}
        Wiadomość: {lead_data.get('message', 'Brak')}
        Status: {lead_data.get('status', 'new')}

        Panel Admina: https://glass-core-467907-e9.ey.r.appspot.com/admin
        """

        return self.send_email(self.admin_email, subject, html_content, text_content)

    def send_lead_confirmation(self, lead_data: Dict[str, Any]) -> bool:
        """Wysyła potwierdzenie do klienta"""
        to_email = lead_data.get("email")
        if not to_email:
            return False

        subject = "✅ Dziękujemy za kontakt - NovaHouse"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; text-align: center; }}
                .content {{ padding: 30px 0; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat {{ text-align: center; }}
                .stat-value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                .stat-label {{ font-size: 12px; color: #666; }}
                .cta {{ background: #667eea; color: white; padding: 15px 30px; text-align: center; border-radius: 8px; margin: 20px 0; }}
                .cta a {{ color: white; text-decoration: none; font-weight: bold; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0; color: #666; font-size: 12px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">Dziękujemy za kontakt! ✨</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">
                        Twoje zapytanie zostało przekazane do naszego zespołu
                    </p>
                </div>

                <div class="content">
                    <p>Cześć <strong>{lead_data.get('name', '')}</strong>!</p>

                    <p>Cieszymy się, że jesteś zainteresowany naszymi usługami wykończeniowymi.
                    Twoje zapytanie właśnie trafiło do naszego zespołu ekspertów.</p>

                    <div class="stats">
                        <div class="stat">
                            <div class="stat-value">30+</div>
                            <div class="stat-label">projektów</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">95%</div>
                            <div class="stat-label">zadowolonych</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">94%</div>
                            <div class="stat-label">przed terminem</div>
                        </div>
                    </div>

                    <p><strong>Co dalej?</strong></p>
                    <ul>
                        <li>Skontaktujemy się z Tobą w ciągu 24h</li>
                        <li>Omówimy Twoje potrzeby i oczekiwania</li>
                        <li>Przygotujemy bezpłatną wycenę</li>
                        <li>Zaproponujemy najlepsze rozwiązania</li>
                    </ul>

                    <div class="cta">
                        <a href="https://novahouse.pl">Zobacz nasze realizacje 📸</a>
                    </div>

                    <p style="color: #666; font-size: 14px;">
                        Masz pytania? Zadzwoń: <strong>+48 585 004 663</strong>
                    </p>
                </div>

                <div class="footer">
                    <p><strong>NovaHouse</strong> - Kompleksowe wykończenie wnętrz</p>
                    <p>Trójmiasto | Warszawa | Wrocław</p>
                    <p>
                        <a href="https://novahouse.pl" style="color: #667eea;">novahouse.pl</a> |
                        <a href="mailto:kontakt@novahouse.pl" style="color: #667eea;">kontakt@novahouse.pl</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Dziękujemy za kontakt!

        Cześć {lead_data.get('name', '')}!

        Twoje zapytanie zostało przekazane do naszego zespołu.
        Skontaktujemy się z Tobą w ciągu 24h.

        NovaHouse - 30+ projektów | 95% zadowolonych | 94% przed terminem

        Telefon: +48 585 004 663
        Web: https://novahouse.pl
        """

        return self.send_email(to_email, subject, html_content, text_content)

    def send_booking_confirmation(self, booking_data: Dict[str, Any]) -> bool:
        """Wysyła potwierdzenie rezerwacji Booksy"""
        to_email = booking_data.get("email")
        if not to_email:
            return False

        subject = f"✅ Potwierdzenie rezerwacji - {booking_data.get('service_name', 'Konsultacja')}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; text-align: center; }}
                .booking-box {{ background: #f9fafb; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea; }}
                .field {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #667eea; }}
                .calendar-add {{ background: #4CAF50; color: white; padding: 12px 24px; text-align: center; border-radius: 8px; margin: 20px 0; }}
                .calendar-add a {{ color: white; text-decoration: none; font-weight: bold; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0; color: #666; font-size: 12px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">✅ Rezerwacja potwierdzona!</h1>
                </div>

                <div class="booking-box">
                    <div class="field">
                        <span class="label">Usługa:</span>
                        {booking_data.get('service_name', 'Konsultacja')}
                    </div>
                    <div class="field">
                        <span class="label">Data:</span>
                        {booking_data.get('date', 'TBD')}
                    </div>
                    <div class="field">
                        <span class="label">Godzina:</span>
                        {booking_data.get('time', 'TBD')}
                    </div>
                    <div class="field">
                        <span class="label">Ekspert:</span>
                        {booking_data.get('staff_name', 'Zespół NovaHouse')}
                    </div>
                </div>

                <p><strong>Przygotuj się na spotkanie:</strong></p>
                <ul>
                    <li>Pomyśl o swoich oczekiwaniach i preferencjach</li>
                    <li>Przygotuj pytania dotyczące projektu</li>
                    <li>Możesz przynieść inspiracje (zdjęcia, materiały)</li>
                </ul>

                <p style="color: #666; font-size: 14px;">
                    Masz pytania? Zadzwoń: <strong>+48 585 004 663</strong>
                </p>

                <div class="footer">
                    <p><strong>NovaHouse</strong> - Kompleksowe wykończenie wnętrz</p>
                    <p>Do zobaczenia! 👋</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(to_email, subject, html_content)

    def send_weekly_report(self, report_data: Dict[str, Any]) -> bool:
        """Wysyła tygodniowy raport analytics do admina"""
        subject = f"📊 Raport tygodniowy NovaHouse - {datetime.now().strftime('%d.%m.%Y')}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 800px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; text-align: center; }}
                .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }}
                .metric-card {{ background: #f9fafb; padding: 20px; border-radius: 8px; text-align: center; border-top: 4px solid #667eea; }}
                .metric-value {{ font-size: 36px; font-weight: bold; color: #667eea; }}
                .metric-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
                .section {{ margin: 30px 0; }}
                .section-title {{ font-size: 18px; font-weight: bold; color: #333; margin-bottom: 15px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0; color: #666; font-size: 12px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">📊 Raport Tygodniowy</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">
                        {report_data.get('period', 'Ostatni tydzień')}
                    </p>
                </div>

                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-value">{report_data.get('total_conversations', 0)}</div>
                        <div class="metric-label">Rozmów</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{report_data.get('total_leads', 0)}</div>
                        <div class="metric-label">Leadów</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{report_data.get('conversion_rate', '0')}%</div>
                        <div class="metric-label">Konwersja</div>
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">📈 Trendy</div>
                    <p>Rozmowy: {report_data.get('conversations_trend', 'stabilne')}</p>
                    <p>Leady: {report_data.get('leads_trend', 'stabilne')}</p>
                </div>

                <div class="section">
                    <div class="section-title">❓ Najczęstsze pytania</div>
                    <ol>
                        {chr(10).join(f'<li>{q}</li>' for q in report_data.get('top_questions', ['Brak danych']))}
                    </ol>
                </div>

                <div class="footer">
                    <p>
                        <a href="https://glass-core-467907-e9.ey.r.appspot.com/admin" style="color: #667eea;">
                            👉 Pełny raport w panelu admina
                        </a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(self.admin_email, subject, html_content)


# Singleton instance
email_service = EmailService()
