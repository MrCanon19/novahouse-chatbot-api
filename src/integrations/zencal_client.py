"""
Zencal API Client
==================
Integracja z systemem rezerwacji Zencal (alternatywa dla Calendly)
"""

import os
from typing import Dict, Optional

import requests


class ZencalClient:
    """Client dla Zencal API - system rezerwacji online"""

    def __init__(self):
        self.api_key = os.getenv("ZENCAL_API_KEY")
        self.workspace_id = os.getenv("ZENCAL_WORKSPACE_ID")
        self.booking_page_url = os.getenv(
            "ZENCAL_BOOKING_URL", "https://zencal.io/novahouse/konsultacja"
        )
        self.api_url = "https://api.zencal.io/v1"

        if not self.api_key:
            print("WARNING: ZENCAL_API_KEY not found in environment variables")
        if not self.workspace_id:
            print("WARNING: ZENCAL_WORKSPACE_ID not found in environment variables")

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Optional[Dict]:
        """Wykonaj request do Zencal API"""

        if not self.api_key:
            print(
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
            print(f"Zencal API Error: {e}")
            return None

    def get_booking_link(
        self, client_name: Optional[str] = None, client_email: Optional[str] = None
    ) -> str:
        if not self.api_key:
            print(
                "ALERT: ZENCAL_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
        if not self.workspace_id:
            print(
                "ALERT: ZENCAL_WORKSPACE_ID not configured! Sprawdź sekret w repozytorium GitHub."
            )
        """
        Pobierz link do rezerwacji Zencal (pre-filled jeśli dane dostępne)

        Returns:
            URL do strony rezerwacji
        """
        link = self.booking_page_url

        # Prefill parametry jeśli dostępne
        params = []
        if client_name:
            params.append(f"name={requests.utils.quote(client_name)}")
        if client_email:
            params.append(f"email={requests.utils.quote(client_email)}")

        if params:
            link += "?" + "&".join(params)

        return link

    def get_available_slots(self, date: str) -> Optional[Dict]:
        if not self.api_key:
            print(
                "ALERT: ZENCAL_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
        if not self.workspace_id:
            print(
                "ALERT: ZENCAL_WORKSPACE_ID not configured! Sprawdź sekret w repozytorium GitHub."
            )
        """
        Pobierz dostępne terminy rezerwacji

        Args:
            date: Data w formacie YYYY-MM-DD

        Returns:
            Dict z dostępnymi slotami czasu
        """
        if not self.api_key or not self.workspace_id:
            print("Zencal not configured, cannot fetch slots")
            return None

        endpoint = f"workspaces/{self.workspace_id}/availability"
        result = self._make_request("GET", f"{endpoint}?date={date}")

        if result and "slots" in result:
            return result
        return None

    def create_booking(self, booking_data: Dict) -> Optional[str]:
        if not self.api_key:
            print(
                "ALERT: ZENCAL_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
        if not self.workspace_id:
            print(
                "ALERT: ZENCAL_WORKSPACE_ID not configured! Sprawdź sekret w repozytorium GitHub."
            )
        """
        Utwórz rezerwację w Zencal

        Args:
            booking_data: {
                'name': str,
                'email': str,
                'phone': str,
                'date': str (YYYY-MM-DD),
                'time': str (HH:MM),
                'notes': str (optional)
            }

        Returns:
            Zencal booking ID lub None
        """
        if not self.api_key or not self.workspace_id:
            print("Zencal not configured, skipping booking creation")
            return None

        endpoint = f"workspaces/{self.workspace_id}/bookings"

        payload = {
            "name": booking_data.get("name"),
            "email": booking_data.get("email"),
            "phone": booking_data.get("phone"),
            "datetime": f"{booking_data.get('date')} {booking_data.get('time')}",
            "notes": booking_data.get("notes", "Rezerwacja z NovaHouse chatbota"),
        }

        result = self._make_request("POST", endpoint, payload)

        if result and "id" in result:
            print(f"Created Zencal booking: {result['id']}")
            return result["id"]

        return None

    def cancel_booking(self, booking_id: str) -> bool:
        if not self.api_key:
            print(
                "ALERT: ZENCAL_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
        if not self.workspace_id:
            print(
                "ALERT: ZENCAL_WORKSPACE_ID not configured! Sprawdź sekret w repozytorium GitHub."
            )
        """
        Anuluj rezerwację w Zencal

        Args:
            booking_id: ID rezerwacji w Zencal

        Returns:
            True jeśli sukces
        """
        if not self.api_key or not self.workspace_id:
            return False

        endpoint = f"workspaces/{self.workspace_id}/bookings/{booking_id}"

        result = self._make_request("DELETE", endpoint)

        return result is not None

    def test_connection(self) -> bool:
        if not self.api_key:
            print(
                "ALERT: ZENCAL_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
        if not self.workspace_id:
            print(
                "ALERT: ZENCAL_WORKSPACE_ID not configured! Sprawdź sekret w repozytorium GitHub."
            )
        """Test połączenia z Zencal API"""

        if not self.api_key or not self.workspace_id:
            print("Zencal not configured")
            return False

        endpoint = f"workspaces/{self.workspace_id}"

        result = self._make_request("GET", endpoint)

        if result:
            print("✅ Zencal connection successful")
            return True
        else:
            print("❌ Zencal connection failed")
            return False
