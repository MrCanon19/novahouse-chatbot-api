"""
Booksy API Client
Handles all interactions with Booksy booking system for consultations
"""

import os
import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class BooksynClient:
    """Client for Booksy API - booking system integration"""

    def __init__(self):
        self.api_key = os.getenv("BOOKSY_API_KEY")
        self.business_id = os.getenv("BOOKSY_BUSINESS_ID")
        self.api_url = "https://api.booksy.com/v1"

        if not self.api_key:
            print("WARNING: BOOKSY_API_KEY not found in environment variables")
        if not self.business_id:
            print("WARNING: BOOKSY_BUSINESS_ID not found in environment variables")

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None
    ) -> Dict:
        """Make a request to Booksy API"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        url = f"{self.api_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, params=params, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data, params=params, timeout=10)
            else:
                return {"errors": [f"Unknown method: {method}"]}

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Booksy API Error: {e}")
            return {"errors": [str(e)]}

    def test_connection(self) -> bool:
        """Test connection to Booksy API"""

        if not self.api_key or not self.business_id:
            return False

        result = self._make_request("GET", f"/businesses/{self.business_id}")

        if "errors" in result:
            print(f"Booksy connection failed: {result['errors']}")
            return False

        if "id" in result:
            print(f"Booksy connected to business: {result.get('name', 'Unknown')}")
            return True

        return False

    def get_available_slots(
        self,
        service_id: str,
        staff_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> List[Dict]:
        """Get available time slots for a service"""

        if not self.api_key or not self.business_id:
            print("Booksy not configured")
            return []

        if not date_from:
            date_from = datetime.now().isoformat()

        if not date_to:
            date_to = (datetime.now() + timedelta(days=30)).isoformat()

        params = {"service_id": service_id, "date_from": date_from, "date_to": date_to}

        if staff_id:
            params["staff_id"] = staff_id

        result = self._make_request(
            "GET", f"/businesses/{self.business_id}/available-slots", params=params
        )

        if "errors" in result:
            print(f"Failed to get available slots: {result['errors']}")
            return []

        return result.get("slots", [])

    def create_booking(
        self,
        client_name: str,
        client_email: str,
        client_phone: str,
        service_id: str,
        start_time: str,
        staff_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[str]:
        """Create a new booking"""

        if not self.api_key or not self.business_id:
            print("Booksy not configured, skipping booking creation")
            return None

        booking_data = {
            "client": {"name": client_name, "email": client_email, "phone": client_phone},
            "service_id": service_id,
            "start_time": start_time,
            "notes": notes or "Konsultacja z Novahouse chatbota",
        }

        if staff_id:
            booking_data["staff_id"] = staff_id

        result = self._make_request(
            "POST", f"/businesses/{self.business_id}/bookings", data=booking_data
        )

        if "errors" in result:
            print(f"Failed to create booking: {result['errors']}")
            return None

        if "id" in result:
            booking_id = result["id"]
            print(f"Created Booksy booking: {booking_id}")
            return booking_id

        return None

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel an existing booking"""

        if not self.api_key or not self.business_id:
            return False

        result = self._make_request(
            "PUT",
            f"/businesses/{self.business_id}/bookings/{booking_id}",
            data={"status": "cancelled"},
        )

        return "errors" not in result

    def get_services(self) -> List[Dict]:
        """Get all available services for the business"""

        if not self.api_key or not self.business_id:
            print("Booksy not configured")
            return []

        result = self._make_request("GET", f"/businesses/{self.business_id}/services")

        if "errors" in result:
            print(f"Failed to get services: {result['errors']}")
            return []

        return result.get("services", [])

    def get_staff(self) -> List[Dict]:
        """Get all staff members for the business"""

        if not self.api_key or not self.business_id:
            print("Booksy not configured")
            return []

        result = self._make_request("GET", f"/businesses/{self.business_id}/staff")

        if "errors" in result:
            print(f"Failed to get staff: {result['errors']}")
            return []

        return result.get("staff", [])
