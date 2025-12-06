import os
import time

import pytest

from src.integrations.monday_client import MondayClient


@pytest.mark.skipif(
    not os.getenv("MONDAY_API_KEY") or not os.getenv("MONDAY_BOARD_ID"),
    reason="Brak MONDAY_API_KEY lub MONDAY_BOARD_ID w środowisku",
)
def test_monday_create_lead_live():
    """Test tworzenia lead'a w Monday.com (live API)"""
    client = MondayClient(api_key=os.getenv("MONDAY_API_KEY"))
    lead_data = {
        "name": "Test Lead Live",
        "email": "test-live@example.com",
        "phone": "+48123456789",
        "message": "Test integracji live - automated test",
        "property_type": "Mieszkanie",
        "budget": "50m2",
        "lead_score": 99,
        "competitor_mentioned": None,
        "next_action": "Kontakt telefoniczny",
    }
    item_id = client.create_lead_item(lead_data)
    assert item_id is not None, "Monday.com nie zwrócił ID itemu (live)"
    print(f"✅ Created Monday item: {item_id}")


@pytest.mark.skipif(
    not os.getenv("MONDAY_API_KEY") or not os.getenv("MONDAY_BOARD_ID"),
    reason="Brak MONDAY_API_KEY lub MONDAY_BOARD_ID w środowisku",
)
def test_monday_full_customer_journey_live():
    """
    Test pełnej ścieżki klienta w Monday.com:
    1. Utworzenie lead'a z niskim score
    2. Utworzenie lead'a z wysokim score (hot lead)
    3. Utworzenie lead'a z competitor mention
    """
    client = MondayClient(api_key=os.getenv("MONDAY_API_KEY"))
    timestamp = int(time.time())

    # 1. Low score lead
    low_score_data = {
        "name": f"Low Score Test {timestamp}",
        "email": f"low-score-{timestamp}@test.com",
        "phone": "+48111111111",
        "message": "Tylko ogólne pytanie o cenę",
        "property_type": "Dom",
        "budget": "nie wiem",
        "lead_score": 25,
        "competitor_mentioned": None,
        "next_action": "Email follow-up",
    }
    low_id = client.create_lead_item(low_score_data)
    assert low_id, "Failed to create low score lead"
    print(f"✅ Low score lead: {low_id} (score: 25)")

    # 2. Hot lead
    hot_lead_data = {
        "name": f"Hot Lead Test {timestamp}",
        "email": f"hot-lead-{timestamp}@test.com",
        "phone": "+48222222222",
        "message": "Chcę już dzisiaj podpisać umowę! Mieszkanie 85m2 w Warszawie, budżet 150k PLN",
        "property_type": "Mieszkanie",
        "budget": "85m2",
        "lead_score": 95,
        "competitor_mentioned": None,
        "next_action": "Natychmiastowy kontakt telefoniczny",
    }
    hot_id = client.create_lead_item(hot_lead_data)
    assert hot_id, "Failed to create hot lead"
    print(f"🔥 Hot lead: {hot_id} (score: 95)")

    # 3. Competitor mention
    competitor_data = {
        "name": f"Competitor Test {timestamp}",
        "email": f"competitor-{timestamp}@test.com",
        "phone": "+48333333333",
        "message": "Porównuję was z BestReno, co możecie zaoferować?",
        "property_type": "Mieszkanie",
        "budget": "65m2",
        "lead_score": 70,
        "competitor_mentioned": "BestReno",
        "next_action": "Konkurencyjna oferta",
    }
    comp_id = client.create_lead_item(competitor_data)
    assert comp_id, "Failed to create competitor lead"
    print(f"⚠️ Competitor mention lead: {comp_id} (vs BestReno)")

    print("\n✅ Pełna ścieżka Monday.com: 3/3 lead'y utworzone")
