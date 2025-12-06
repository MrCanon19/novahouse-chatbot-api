import os

import pytest
from src.integrations.monday_client import MondayClient


@pytest.mark.skipif(
    not os.getenv("MONDAY_API_KEY") or not os.getenv("MONDAY_BOARD_ID"),
    reason="Brak MONDAY_API_KEY lub MONDAY_BOARD_ID w środowisku",
)
def test_monday_create_lead_live():
    client = MondayClient(api_key=os.getenv("MONDAY_API_KEY"))
    lead_data = {
        "name": "Test Lead",
        "email": "test-lead@example.com",
        "phone": "+48123456789",
        "message": "Test integracji live",
        "property_type": "Mieszkanie",
        "budget": "50m2",
        "lead_score": 99,
        "competitor_mentioned": None,
        "next_action": "Kontakt telefoniczny",
    }
    item_id = client.create_lead_item(lead_data)
    assert item_id is not None, "Monday.com nie zwrócił ID itemu (live)"
