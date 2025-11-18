"""
Google Calendar Integration for NovaHouse Chatbot
Automatyczne bookowanie spotkań z konsultantami
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Google Calendar API (symulacja - w produkcji użyj google-api-python-client)
class GoogleCalendarIntegration:
    """Integracja z Google Calendar dla automatycznego bookowania spotkań"""
    
    def __init__(self):
        self.calendar_id = os.environ.get('GOOGLE_CALENDAR_ID', 'primary')
        self.service_account_key = os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY')
        self.consultant_calendars = {
            'projektant': 'projektant@novahouse.pl',
            'konsultant_sprzedazy': 'sprzedaz@novahouse.pl',
            'specjalista_techniczny': 'tech@novahouse.pl'
        }
        
    def get_available_slots(self, consultant_type: str = 'konsultant_sprzedazy', 
                           days_ahead: int = 14) -> List[Dict]:
        """
        Pobranie dostępnych terminów dla konsultanta
        
        Args:
            consultant_type: Typ konsultanta (projektant, konsultant_sprzedazy, specjalista_techniczny)
            days_ahead: Ile dni do przodu sprawdzać dostępność
            
        Returns:
            Lista dostępnych slotów czasowych
        """
        try:
            # Symulacja dostępnych terminów (w produkcji: zapytanie do Google Calendar API)
            available_slots = []
            
            # Generowanie przykładowych dostępnych terminów
            start_date = datetime.now() + timedelta(days=1)  # Od jutra
            
            for day in range(days_ahead):
                current_date = start_date + timedelta(days=day)
                
                # Pomijamy weekendy
                if current_date.weekday() >= 5:  # 5=sobota, 6=niedziela
                    continue
                
                # Godziny pracy: 9:00-17:00
                for hour in [9, 10, 11, 13, 14, 15, 16]:  # Przerwa obiadowa 12-13
                    slot_time = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                    
                    # Symulacja dostępności (80% slotów dostępnych)
                    import random
                    if random.random() > 0.2:  # 80% szans na dostępność
                        available_slots.append({
                            'datetime': slot_time.isoformat(),
                            'formatted_date': slot_time.strftime('%d.%m.%Y'),
                            'formatted_time': slot_time.strftime('%H:%M'),
                            'consultant_type': consultant_type,
                            'duration_minutes': 60,
                            'meeting_type': 'konsultacja'
                        })
            
            return available_slots[:20]  # Maksymalnie 20 najbliższych terminów
            
        except Exception as e:
            logging.error(f"Błąd pobierania dostępnych terminów: {e}")
            return []
    
    def book_appointment(self, client_data: Dict, slot_datetime: str, 
                        consultant_type: str = 'konsultant_sprzedazy') -> Dict:
        """
        Rezerwacja spotkania w kalendarzu
        
        Args:
            client_data: Dane klienta (imię, telefon, email, etc.)
            slot_datetime: Data i godzina spotkania (ISO format)
            consultant_type: Typ konsultanta
            
        Returns:
            Wynik rezerwacji
        """
        try:
            # Walidacja danych
            required_fields = ['phone']
            for field in required_fields:
                if field not in client_data or not client_data[field]:
                    return {
                        'success': False,
                        'error': f'Brak wymaganego pola: {field}',
                        'error_code': 'MISSING_REQUIRED_FIELD'
                    }
            
            # Parsowanie daty
            appointment_datetime = datetime.fromisoformat(slot_datetime.replace('Z', '+00:00'))
            
            # Przygotowanie danych spotkania
            meeting_data = {
                'summary': f'Konsultacja NovaHouse - {client_data.get("name", "Klient")}',
                'description': self._generate_meeting_description(client_data),
                'start': {
                    'dateTime': appointment_datetime.isoformat(),
                    'timeZone': 'Europe/Warsaw'
                },
                'end': {
                    'dateTime': (appointment_datetime + timedelta(hours=1)).isoformat(),
                    'timeZone': 'Europe/Warsaw'
                },
                'attendees': [
                    {'email': self.consultant_calendars.get(consultant_type, 'konsultant@novahouse.pl')},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 24h wcześniej
                        {'method': 'popup', 'minutes': 30},       # 30min wcześniej
                    ],
                }
            }
            
            # Symulacja tworzenia wydarzenia (w produkcji: Google Calendar API)
            event_id = f"novahouse_{int(appointment_datetime.timestamp())}"
            
            # Logowanie rezerwacji
            logging.info(f"Zarezerwowano spotkanie: {event_id} dla {client_data.get('phone')}")
            
            return {
                'success': True,
                'event_id': event_id,
                'meeting_link': f'https://calendar.google.com/event?eid={event_id}',
                'appointment_datetime': appointment_datetime.strftime('%d.%m.%Y o %H:%M'),
                'consultant_email': self.consultant_calendars.get(consultant_type),
                'message': f'Spotkanie zostało zarezerwowane na {appointment_datetime.strftime("%d.%m.%Y o %H:%M")}'
            }
            
        except Exception as e:
            logging.error(f"Błąd rezerwacji spotkania: {e}")
            return {
                'success': False,
                'error': str(e),
                'error_code': 'BOOKING_ERROR'
            }
    
    def _generate_meeting_description(self, client_data: Dict) -> str:
        """Generowanie opisu spotkania na podstawie danych klienta"""
        
        description_parts = [
            "🏠 Konsultacja NovaHouse - Wykończenia wnętrz",
            "",
            "📋 Dane klienta:",
        ]
        
        if client_data.get('name'):
            description_parts.append(f"• Imię: {client_data['name']}")
        
        if client_data.get('phone'):
            description_parts.append(f"• Telefon: {client_data['phone']}")
        
        if client_data.get('email'):
            description_parts.append(f"• Email: {client_data['email']}")
        
        if client_data.get('property_size'):
            description_parts.append(f"• Powierzchnia: {client_data['property_size']}")
        
        if client_data.get('property_type'):
            description_parts.append(f"• Typ nieruchomości: {client_data['property_type']}")
        
        if client_data.get('location'):
            description_parts.append(f"• Lokalizacja: {client_data['location']}")
        
        if client_data.get('interested_package'):
            description_parts.append(f"• Interesujący pakiet: {client_data['interested_package']}")
        
        if client_data.get('budget'):
            description_parts.append(f"• Budżet: {client_data['budget']}")
        
        if client_data.get('timeline'):
            description_parts.append(f"• Termin realizacji: {client_data['timeline']}")
        
        if client_data.get('additional_info'):
            description_parts.extend([
                "",
                "💬 Dodatkowe informacje:",
                client_data['additional_info']
            ])
        
        description_parts.extend([
            "",
            "🎯 Cel spotkania:",
            "• Prezentacja pakietów wykończeniowych",
            "• Wstępna wycena kosztów",
            "• Omówienie harmonogramu realizacji",
            "• Odpowiedzi na pytania klienta",
            "",
            "📞 W razie pytań: kontakt@novahouse.pl"
        ])
        
        return "\n".join(description_parts)
    
    def cancel_appointment(self, event_id: str) -> Dict:
        """
        Anulowanie spotkania
        
        Args:
            event_id: ID wydarzenia w kalendarzu
            
        Returns:
            Wynik anulowania
        """
        try:
            # Symulacja anulowania (w produkcji: Google Calendar API)
            logging.info(f"Anulowano spotkanie: {event_id}")
            
            return {
                'success': True,
                'message': 'Spotkanie zostało anulowane'
            }
            
        except Exception as e:
            logging.error(f"Błąd anulowania spotkania: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def reschedule_appointment(self, event_id: str, new_datetime: str) -> Dict:
        """
        Przełożenie spotkania na inny termin
        
        Args:
            event_id: ID wydarzenia w kalendarzu
            new_datetime: Nowa data i godzina (ISO format)
            
        Returns:
            Wynik przełożenia
        """
        try:
            new_appointment_datetime = datetime.fromisoformat(new_datetime.replace('Z', '+00:00'))
            
            # Symulacja przełożenia (w produkcji: Google Calendar API)
            logging.info(f"Przełożono spotkanie {event_id} na {new_appointment_datetime}")
            
            return {
                'success': True,
                'new_datetime': new_appointment_datetime.strftime('%d.%m.%Y o %H:%M'),
                'message': f'Spotkanie zostało przełożone na {new_appointment_datetime.strftime("%d.%m.%Y o %H:%M")}'
            }
            
        except Exception as e:
            logging.error(f"Błąd przełożenia spotkania: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Funkcje pomocnicze dla chatbota
def get_calendar_integration():
    """Pobranie instancji integracji z kalendarzem"""
    return GoogleCalendarIntegration()

def format_available_slots_for_chat(slots: List[Dict]) -> str:
    """Formatowanie dostępnych terminów dla chatbota"""
    if not slots:
        return "Przepraszam, obecnie nie ma dostępnych terminów. Skontaktuj się z nami telefonicznie."
    
    formatted_slots = ["📅 **Dostępne terminy konsultacji:**", ""]
    
    current_date = None
    for i, slot in enumerate(slots[:10]):  # Maksymalnie 10 terminów
        slot_date = slot['formatted_date']
        slot_time = slot['formatted_time']
        
        if slot_date != current_date:
            if current_date is not None:
                formatted_slots.append("")
            formatted_slots.append(f"**{slot_date}:**")
            current_date = slot_date
        
        formatted_slots.append(f"• {slot_time}")
    
    formatted_slots.extend([
        "",
        "Aby zarezerwować termin, napisz: **'Rezerwuję [data] [godzina]'**",
        "Przykład: *Rezerwuję 15.10.2024 10:00*"
    ])
    
    return "\n".join(formatted_slots)

