"""
Zencal API Client
==================
Integracja z systemem rezerwacji Zencal (alternatywa dla Calendly)
"""

import logging
import os
from typing import Dict, Optional

import requests


class ZencalClient:
    """Client dla Zencal API - system rezerwacji online"""

    def __init__(self, api_key: Optional[str] = None, workspace_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("ZENCAL_API_KEY")
        self.workspace_id = workspace_id or os.getenv("ZENCAL_WORKSPACE_ID")
        self.booking_page_url = os.getenv(
            "ZENCAL_BOOKING_URL", "https://zencal.io/novahouse/konsultacja"
        )
        self.api_url = "https://api.zencal.io/v1"

        if not self.api_key:
            logging.warning("WARNING: ZENCAL_API_KEY not found in environment variables")
        if not self.workspace_id:
            logging.warning("WARNING: ZENCAL_WORKSPACE_ID not found in environment variables")

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Optional[Dict]:
        """Wykonaj request do Zencal API"""

        if not self.api_key:
            logging.warning(
                "ALERT: ZENCAL_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
            return None

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        url = f"{self.api_url}/{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return None

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logging.error(f"Zencal API Error: {e}", exc_info=True)
            return None

    def get_booking_link(
        self,
        client_name: Optional[str] = None,
        client_email: Optional[str] = None,
        consultant_booking_url: Optional[str] = None,
    ) -> str:
        """
        Pobierz link do rezerwacji z pre-filled danymi

        Args:
            client_name: Imię klienta (optional)
            client_email: Email klienta (optional)
            consultant_booking_url: Unikalny URL konsultanta (jeśli przypisany do konkretnego konsultanta)

        Returns:
            URL do strony rezerwacji Zencal
        """
        # Jeśli mamy przypisanego konsultanta, użyj jego unikalnego URL
        base_url = consultant_booking_url or self.booking_page_url

        # Dodaj parametry do URL jeśli dostępne
        params = []
        if client_name:
            params.append(f"name={client_name}")
        if client_email:
            params.append(f"email={client_email}")

        if params:
            return f"{base_url}?{'&'.join(params)}"
        return base_url

    def get_available_slots(self, date: str) -> Optional[Dict]:
        """
        Pobierz dostępne terminy dla danej daty

        Args:
            date: Data w formacie YYYY-MM-DD

        Returns:
            Dict z dostępnymi slotami lub None
        """
        if not self.api_key or not self.workspace_id:
            return None

        endpoint = f"workspaces/{self.workspace_id}/availability"
        params = {"date": date}

        result = self._make_request("GET", endpoint)

        if result and "slots" in result:
            return result
        return None

    def create_booking(self, booking_data: Dict) -> Optional[str]:
        """
        Utwórz rezerwację w Zencal

        Args:
            booking_data: {
                'name': str,
                'email': str,
                'phone': str,
                'date': str (YYYY-MM-DD),
                'time': str (HH:MM),
                'notes': str (optional),
                'zencal_user_id': str (optional) - ID konsultanta w Zencal
            }

        Returns:
            Zencal booking ID lub None
        """
        if not self.api_key or not self.workspace_id:
            logging.warning("Zencal not configured, skipping booking creation")
            return None

        endpoint = f"workspaces/{self.workspace_id}/bookings"

        payload = {
            "name": booking_data.get("name"),
            "email": booking_data.get("email"),
            "phone": booking_data.get("phone"),
            "datetime": f"{booking_data.get('date')} {booking_data.get('time')}",
            "notes": booking_data.get("notes", "Rezerwacja z NovaHouse chatbota"),
        }

        # Jeśli mamy przypisanego konsultanta, dodaj jego ID do payload
        if booking_data.get("zencal_user_id"):
            payload["user_id"] = booking_data.get("zencal_user_id")

        result = self._make_request("POST", endpoint, payload)

        if result and "id" in result:
            logging.info(f"Created Zencal booking: {result['id']}")
            return result["id"]

        return None

    def get_team_members(self) -> Optional[list]:
        """
        Pobierz listę członków zespołu z Zencal

        Returns:
            Lista członków zespołu lub None
        """
        if not self.api_key or not self.workspace_id:
            return None

        endpoint = f"workspaces/{self.workspace_id}/team-members"

        result = self._make_request("GET", endpoint)

        if result and "members" in result:
            return result["members"]
        return None

    def cancel_booking(self, booking_id: str) -> bool:
        """
        Anuluj rezerwację w Zencal

        Args:
            booking_id: ID rezerwacji do anulowania

        Returns:
            True jeśli anulowano, False w przeciwnym razie
        """
        if not self.api_key or not self.workspace_id:
            return False

        endpoint = f"workspaces/{self.workspace_id}/bookings/{booking_id}"

        result = self._make_request("DELETE", endpoint)

        return result is not None

    def test_connection(self) -> bool:
        """
        Test połączenia z Zencal API

        Returns:
            True jeśli połączenie działa, False w przeciwnym razie
        """
        if not self.api_key or not self.workspace_id:
            return False

        try:
            # Spróbuj pobrać informacje o workspace
            endpoint = f"workspaces/{self.workspace_id}"
            result = self._make_request("GET", endpoint)
            return result is not None
        except Exception:
            return False

