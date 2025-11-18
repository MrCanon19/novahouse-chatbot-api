"""
Email Automation System for NovaHouse Chatbot
Automatyczne wysyłanie emaili follow-up po rozmowach
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import json

class EmailAutomation:
    """System automatyzacji emaili dla NovaHouse"""
    
    def __init__(self):
        # Konfiguracja SMTP
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = os.environ.get('SMTP_USERNAME', 'chatbot@novahouse.pl')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', 'chatbot@novahouse.pl')
        self.from_name = os.environ.get('FROM_NAME', 'NovaHouse Chatbot')
        
        # Szablony emaili
        self.email_templates = self._load_email_templates()
        
    def _load_email_templates(self) -> Dict:
        """Ładowanie szablonów emaili"""
        return {
            'welcome_after_chat': {
                'subject': '🏠 Dziękujemy za rozmowę z NovaHouse!',
                'template': 'welcome_after_chat.html'
            },
            'appointment_confirmation': {
                'subject': '📅 Potwierdzenie spotkania - NovaHouse',
                'template': 'appointment_confirmation.html'
            },
            'appointment_reminder': {
                'subject': '⏰ Przypomnienie o spotkaniu jutro - NovaHouse',
                'template': 'appointment_reminder.html'
            },
            'follow_up_no_appointment': {
                'subject': '💡 Masz jeszcze pytania o wykończenia? - NovaHouse',
                'template': 'follow_up_no_appointment.html'
            },
            'satisfaction_survey': {
                'subject': '⭐ Jak oceniasz naszą obsługę? - NovaHouse',
                'template': 'satisfaction_survey.html'
            }
        }
    
    def send_welcome_email(self, client_data: Dict) -> Dict:
        """
        Wysłanie emaila powitalnego po rozmowie z chatbotem
        
        Args:
            client_data: Dane klienta z rozmowy
            
        Returns:
            Wynik wysyłania
        """
        try:
            if not client_data.get('email'):
                return {'success': False, 'error': 'Brak adresu email'}
            
            # Przygotowanie danych do szablonu
            template_data = {
                'client_name': client_data.get('name', 'Szanowny Kliencie'),
                'chat_summary': self._generate_chat_summary(client_data),
                'next_steps': self._generate_next_steps(client_data),
                'contact_info': self._get_contact_info(),
                'date': datetime.now().strftime('%d.%m.%Y')
            }
            
            # Generowanie treści emaila
            html_content = self._generate_email_content('welcome_after_chat', template_data)
            
            # Wysłanie emaila
            result = self._send_email(
                to_email=client_data['email'],
                subject=self.email_templates['welcome_after_chat']['subject'],
                html_content=html_content,
                template_data=template_data
            )
            
            if result['success']:
                logging.info(f"Wysłano email powitalny do {client_data['email']}")
            
            return result
            
        except Exception as e:
            logging.error(f"Błąd wysyłania emaila powitalnego: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_appointment_confirmation(self, client_data: Dict, appointment_data: Dict) -> Dict:
        """
        Wysłanie potwierdzenia spotkania
        
        Args:
            client_data: Dane klienta
            appointment_data: Dane spotkania (data, godzina, konsultant)
            
        Returns:
            Wynik wysyłania
        """
        try:
            if not client_data.get('email'):
                return {'success': False, 'error': 'Brak adresu email'}
            
            # Przygotowanie danych do szablonu
            template_data = {
                'client_name': client_data.get('name', 'Szanowny Kliencie'),
                'appointment_date': appointment_data.get('formatted_date'),
                'appointment_time': appointment_data.get('formatted_time'),
                'consultant_name': appointment_data.get('consultant_name', 'Konsultant NovaHouse'),
                'meeting_location': appointment_data.get('location', 'Showroom NovaHouse'),
                'meeting_address': 'ul. Przykładowa 123, 00-001 Warszawa',
                'calendar_link': appointment_data.get('calendar_link', ''),
                'contact_info': self._get_contact_info(),
                'preparation_tips': self._get_preparation_tips()
            }
            
            # Generowanie treści emaila
            html_content = self._generate_email_content('appointment_confirmation', template_data)
            
            # Wysłanie emaila
            result = self._send_email(
                to_email=client_data['email'],
                subject=self.email_templates['appointment_confirmation']['subject'],
                html_content=html_content,
                template_data=template_data
            )
            
            if result['success']:
                logging.info(f"Wysłano potwierdzenie spotkania do {client_data['email']}")
            
            return result
            
        except Exception as e:
            logging.error(f"Błąd wysyłania potwierdzenia spotkania: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_appointment_reminder(self, client_data: Dict, appointment_data: Dict) -> Dict:
        """
        Wysłanie przypomnienia o spotkaniu (24h wcześniej)
        
        Args:
            client_data: Dane klienta
            appointment_data: Dane spotkania
            
        Returns:
            Wynik wysyłania
        """
        try:
            if not client_data.get('email'):
                return {'success': False, 'error': 'Brak adresu email'}
            
            # Przygotowanie danych do szablonu
            template_data = {
                'client_name': client_data.get('name', 'Szanowny Kliencie'),
                'appointment_date': appointment_data.get('formatted_date'),
                'appointment_time': appointment_data.get('formatted_time'),
                'consultant_name': appointment_data.get('consultant_name', 'Konsultant NovaHouse'),
                'meeting_location': appointment_data.get('location', 'Showroom NovaHouse'),
                'meeting_address': 'ul. Przykładowa 123, 00-001 Warszawa',
                'contact_info': self._get_contact_info(),
                'what_to_bring': self._get_what_to_bring_list()
            }
            
            # Generowanie treści emaila
            html_content = self._generate_email_content('appointment_reminder', template_data)
            
            # Wysłanie emaila
            result = self._send_email(
                to_email=client_data['email'],
                subject=self.email_templates['appointment_reminder']['subject'],
                html_content=html_content,
                template_data=template_data
            )
            
            if result['success']:
                logging.info(f"Wysłano przypomnienie o spotkaniu do {client_data['email']}")
            
            return result
            
        except Exception as e:
            logging.error(f"Błąd wysyłania przypomnienia: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_follow_up_email(self, client_data: Dict, days_after: int = 3) -> Dict:
        """
        Wysłanie emaila follow-up dla klientów bez umówionego spotkania
        
        Args:
            client_data: Dane klienta
            days_after: Ile dni po rozmowie wysłać
            
        Returns:
            Wynik wysyłania
        """
        try:
            if not client_data.get('email'):
                return {'success': False, 'error': 'Brak adresu email'}
            
            # Przygotowanie danych do szablonu
            template_data = {
                'client_name': client_data.get('name', 'Szanowny Kliencie'),
                'chat_topics': self._extract_chat_topics(client_data),
                'special_offer': self._get_current_special_offer(),
                'portfolio_examples': self._get_portfolio_examples(),
                'contact_info': self._get_contact_info(),
                'calendar_link': 'https://calendly.com/novahouse/konsultacja'
            }
            
            # Generowanie treści emaila
            html_content = self._generate_email_content('follow_up_no_appointment', template_data)
            
            # Wysłanie emaila
            result = self._send_email(
                to_email=client_data['email'],
                subject=self.email_templates['follow_up_no_appointment']['subject'],
                html_content=html_content,
                template_data=template_data
            )
            
            if result['success']:
                logging.info(f"Wysłano follow-up email do {client_data['email']}")
            
            return result
            
        except Exception as e:
            logging.error(f"Błąd wysyłania follow-up: {e}")
            return {'success': False, 'error': str(e)}
    
    def _send_email(self, to_email: str, subject: str, html_content: str, 
                   template_data: Dict, attachments: List = None) -> Dict:
        """
        Wysłanie emaila przez SMTP
        
        Args:
            to_email: Adres odbiorcy
            subject: Temat emaila
            html_content: Treść HTML
            template_data: Dane do szablonu
            attachments: Lista załączników
            
        Returns:
            Wynik wysyłania
        """
        try:
            # Tworzenie wiadomości
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Dodanie treści HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Dodanie załączników
            if attachments:
                for attachment in attachments:
                    self._add_attachment(msg, attachment)
            
            # Wysłanie przez SMTP
            if self.smtp_password:  # Tylko jeśli skonfigurowane
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
                
                return {
                    'success': True,
                    'message': f'Email wysłany do {to_email}',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Symulacja wysyłania (dla testów)
                logging.info(f"SYMULACJA: Email do {to_email} - {subject}")
                return {
                    'success': True,
                    'message': f'Email (symulacja) wysłany do {to_email}',
                    'timestamp': datetime.now().isoformat(),
                    'simulated': True
                }
                
        except Exception as e:
            logging.error(f"Błąd wysyłania emaila: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_email_content(self, template_name: str, template_data: Dict) -> str:
        """Generowanie treści emaila na podstawie szablonu"""
        
        # Podstawowe szablony HTML (w produkcji: ładowanie z plików)
        templates = {
            'welcome_after_chat': """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
                    .content { padding: 20px; }
                    .footer { background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }
                    .button { background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🏠 NovaHouse</h1>
                    <p>Dziękujemy za rozmowę!</p>
                </div>
                <div class="content">
                    <p>Cześć {client_name}!</p>
                    
                    <p>Dziękujemy za rozmowę z naszym chatbotem. Cieszymy się, że interesują Cię nasze usługi wykończenia wnętrz.</p>
                    
                    <h3>📋 Podsumowanie rozmowy:</h3>
                    <p>{chat_summary}</p>
                    
                    <h3>🎯 Następne kroki:</h3>
                    <p>{next_steps}</p>
                    
                    <p><a href="https://calendly.com/novahouse/konsultacja" class="button">Umów bezpłatną konsultację</a></p>
                    
                    <h3>📞 Kontakt:</h3>
                    <p>{contact_info}</p>
                    
                    <p>Pozdrawiamy,<br>Zespół NovaHouse</p>
                </div>
                <div class="footer">
                    <p>NovaHouse - Twój partner w wykańczaniu wnętrz | {date}</p>
                </div>
            </body>
            </html>
            """,
            
            'appointment_confirmation': """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
                    .content { padding: 20px; }
                    .appointment-box { background: #f8f9fa; border-left: 4px solid #667eea; padding: 15px; margin: 15px 0; }
                    .footer { background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }
                    .button { background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📅 Potwierdzenie spotkania</h1>
                    <p>NovaHouse</p>
                </div>
                <div class="content">
                    <p>Cześć {client_name}!</p>
                    
                    <p>Potwierdzamy rezerwację Twojego spotkania z naszym konsultantem.</p>
                    
                    <div class="appointment-box">
                        <h3>📅 Szczegóły spotkania:</h3>
                        <p><strong>Data:</strong> {appointment_date}</p>
                        <p><strong>Godzina:</strong> {appointment_time}</p>
                        <p><strong>Konsultant:</strong> {consultant_name}</p>
                        <p><strong>Miejsce:</strong> {meeting_location}</p>
                        <p><strong>Adres:</strong> {meeting_address}</p>
                    </div>
                    
                    <p><a href="{calendar_link}" class="button">Dodaj do kalendarza</a></p>
                    
                    <h3>💡 Jak się przygotować:</h3>
                    <p>{preparation_tips}</p>
                    
                    <h3>📞 Kontakt:</h3>
                    <p>{contact_info}</p>
                    
                    <p>Do zobaczenia!<br>Zespół NovaHouse</p>
                </div>
                <div class="footer">
                    <p>NovaHouse - Twój partner w wykańczaniu wnętrz</p>
                </div>
            </body>
            </html>
            """
        }
        
        template = templates.get(template_name, templates['welcome_after_chat'])
        return template.format(**template_data)
    
    def _generate_chat_summary(self, client_data: Dict) -> str:
        """Generowanie podsumowania rozmowy"""
        summary_parts = []
        
        if client_data.get('interested_package'):
            summary_parts.append(f"• Interesujący pakiet: {client_data['interested_package']}")
        
        if client_data.get('property_size'):
            summary_parts.append(f"• Powierzchnia: {client_data['property_size']}")
        
        if client_data.get('property_type'):
            summary_parts.append(f"• Typ nieruchomości: {client_data['property_type']}")
        
        if client_data.get('location'):
            summary_parts.append(f"• Lokalizacja: {client_data['location']}")
        
        if not summary_parts:
            return "Rozmawialiśmy o naszych usługach wykończenia wnętrz."
        
        return "<br>".join(summary_parts)
    
    def _generate_next_steps(self, client_data: Dict) -> str:
        """Generowanie następnych kroków"""
        if client_data.get('appointment_booked'):
            return "Spotkanie zostało umówione. Szczegóły znajdziesz w osobnym emailu."
        else:
            return "Zachęcamy do umówienia bezpłatnej konsultacji, podczas której omówimy Twoje potrzeby i przedstawimy najlepsze rozwiązania."
    
    def _get_contact_info(self) -> str:
        """Informacje kontaktowe"""
        return """
        📧 Email: kontakt@novahouse.pl<br>
        📞 Telefon: +48 123 456 789<br>
        🌐 Strona: www.novahouse.pl<br>
        📍 Showroom: ul. Przykładowa 123, 00-001 Warszawa
        """
    
    def _get_preparation_tips(self) -> str:
        """Wskazówki przygotowania do spotkania"""
        return """
        • Przygotuj listę pytań o wykończenia<br>
        • Pomyśl o swoich preferencjach stylistycznych<br>
        • Jeśli masz inspiracje (zdjęcia), zabierz je ze sobą<br>
        • Przygotuj informacje o budżecie i terminach
        """
    
    def _extract_chat_topics(self, client_data: Dict) -> str:
        """Wyciągnięcie tematów z rozmowy"""
        return "wykończenia wnętrz, pakiety, wycena"
    
    def _get_current_special_offer(self) -> str:
        """Aktualna oferta specjalna"""
        return "Bezpłatna konsultacja projektanta przy wyborze pakietu Express Plus!"
    
    def _get_portfolio_examples(self) -> str:
        """Przykłady z portfolio"""
        return "Sprawdź nasze najnowsze realizacje na www.novahouse.pl/portfolio"
    
    def _get_what_to_bring_list(self) -> str:
        """Lista rzeczy do zabrania na spotkanie"""
        return """
        • Dokumenty techniczne mieszkania/domu<br>
        • Zdjęcia inspiracji (jeśli masz)<br>
        • Notatnik na pytania<br>
        • Informacje o budżecie
        """

# Funkcje pomocnicze dla chatbota
def get_email_automation():
    """Pobranie instancji automatyzacji emaili"""
    return EmailAutomation()

def send_post_chat_email(client_data: Dict) -> Dict:
    """Wysłanie emaila po rozmowie z chatbotem"""
    email_automation = get_email_automation()
    return email_automation.send_welcome_email(client_data)

