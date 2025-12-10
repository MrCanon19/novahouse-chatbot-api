"""
Monday.com API Client
Handles all interactions with Monday.com boards
"""

import json
import logging
import os
from typing import Dict, Optional

import requests
from pybreaker import CircuitBreaker

from src.services.slow_query_logger import log_slow_query

logger = logging.getLogger(__name__)

# Circuit breaker for Monday.com API (fail-fast on repeated failures)
monday_breaker = CircuitBreaker(
    fail_max=5,  # Open after 5 failures
    reset_timeout=60,  # Wait 60 seconds before attempting recovery
    listeners=[],
)
logger.info("✅ Monday.com circuit breaker initialized (fail_max=5, reset_timeout=60s)")


class MondayClient:
    """Client for Monday.com GraphQL API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MONDAY_API_KEY")
        self.board_id = os.getenv("MONDAY_BOARD_ID")
        self.api_url = "https://api.monday.com/v2"

        if not self.api_key:
            print(
                "ALERT: MONDAY_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
        if not self.board_id:
            print("ALERT: MONDAY_BOARD_ID not configured! Sprawdź sekret w repozytorium GitHub.")

    @log_slow_query(threshold_ms=500, query_type="monday")
    def _make_request(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """
        Make a GraphQL request to Monday.com API (WITH CIRCUIT BREAKER)

        Circuit breaker opens after 5 consecutive failures, preventing cascading
        failures when Monday.com API is down or rate-limited.
        """

        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}

        data = {"query": query}

        if variables:
            data["variables"] = variables

        try:

            @monday_breaker
            def call_monday():
                return requests.post(self.api_url, json=data, headers=headers, timeout=10)

            response = call_monday()
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.warning(f"⚠️  Monday.com API Error: {e} (circuit breaker may be open)")
            return {"errors": [str(e)]}

    def create_lead_item(self, lead_data: Dict) -> Optional[str]:
        """Create a new item on Monday.com board"""

        if not self.api_key:
            print(
                "ALERT: MONDAY_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
        if not self.board_id:
            print("ALERT: MONDAY_BOARD_ID not configured! Sprawdź sekret w repozytorium GitHub.")
        if not self.api_key or not self.board_id:
            print("Monday.com not configured, skipping lead creation")
            return None

        item_name = lead_data.get("name", "Nowy Lead")

        column_values = {}

        if lead_data.get("email"):
            column_values["email"] = {"email": lead_data["email"], "text": lead_data["email"]}

        if lead_data.get("phone"):
            column_values["phone"] = lead_data["phone"]

        if lead_data.get("message"):
            column_values["text"] = lead_data["message"]

        # Kwalifikacja - jeśli dostępne
        if lead_data.get("recommended_package"):
            column_values["package"] = lead_data.get("recommended_package")

        if lead_data.get("confidence_score"):
            column_values["confidence"] = str(lead_data.get("confidence_score"))

        if lead_data.get("property_type"):
            column_values["property_type"] = lead_data.get("property_type")

        if lead_data.get("budget"):
            column_values["budget"] = lead_data.get("budget")

        if lead_data.get("interior_style"):
            column_values["interior_style"] = lead_data.get("interior_style")

        # Enterprise features
        if lead_data.get("lead_score") is not None:
            column_values["lead_score"] = str(lead_data.get("lead_score"))

        if lead_data.get("competitor_mentioned"):
            column_values["competitor_mentioned"] = lead_data.get("competitor_mentioned")

        if lead_data.get("next_action"):
            column_values["next_action"] = lead_data.get("next_action")

        # Status - domyślnie "Nowy Lead"
        column_values["status"] = "New Lead"

        mutation = """
        mutation ($boardId: ID!, $itemName: String!, $columnValues: JSON!) {
            create_item (
                board_id: $boardId,
                item_name: $itemName,
                column_values: $columnValues
            ) {
                id
                name
            }
        }
        """

        variables = {
            "boardId": int(self.board_id),
            "itemName": item_name,
            "columnValues": json.dumps(column_values),
        }

        result = self._make_request(mutation, variables)

        if "errors" in result:
            print(f"Failed to create Monday.com item: {result['errors']}")
            return None

        if "data" in result and "create_item" in result["data"]:
            item_id = result["data"]["create_item"]["id"]
            print(f"Created Monday.com item: {item_id}")
            return item_id

        return None

    def create_lead_item_with_qualification(
        self, lead_data: Dict, qualification_result: Dict
    ) -> Optional[str]:
        """Create a lead item with qualification data from questionnaire"""

        enriched_data = {
            **lead_data,
            "recommended_package": qualification_result.get("recommended_package"),
            "confidence_score": qualification_result.get("confidence", 0),
            "property_type": qualification_result.get("property_type"),
            "budget": qualification_result.get("budget"),
            "interior_style": qualification_result.get("interior_style"),
        }

        return self.create_lead_item(enriched_data)

    def test_connection(self) -> bool:
        """Test connection to Monday.com API"""

        if not self.api_key:
            print(
                "ALERT: MONDAY_API_KEY not configured or expired! Sprawdź sekret w repozytorium GitHub."
            )
            return False

        query = """
        query {
            me {
                id
                name
                email
            }
        }
        """

        result = self._make_request(query)

        if "errors" in result:
            print(f"Monday.com connection failed: {result['errors']}")
            return False

        if "data" in result and "me" in result["data"]:
            user = result["data"]["me"]
            print(f"Monday.com connected as: {user.get('name')} ({user.get('email')})")
            return True

        return False

    def update_item_status(self, item_id, status):
        """Update item status on Monday.com"""
        if not self.api_key:
            print(
                "ALERT: MONDAY_API_KEY not configured lub wygasł! Sprawdź sekret w repozytorium GitHub."
            )
            return False
        if not self.board_id:
            print("ALERT: MONDAY_BOARD_ID not configured! Sprawdź sekret w repozytorium GitHub.")
            return False

        status_map = {
            "new": "New Lead",
            "contacted": "Contacted",
            "qualified": "Qualified",
            "converted": "Done",
            "lost": "Stuck",
        }

        status_label = status_map.get(status, status)

        mutation = """
        mutation ($boardId: ID!, $itemId: ID!, $columnId: String!, $value: JSON!) {
            change_column_value(
                board_id: $boardId,
                item_id: $itemId,
                column_id: $columnId,
                value: $value
            ) {
                id
            }
        }
        """

        variables = {
            "boardId": int(self.board_id),
            "itemId": int(item_id),
            "columnId": "status",
            "value": f'{{"label":"{status_label}"}}',
        }

        result = self._make_request(mutation, variables)
        return "errors" not in result
