import os

import pytest

from src.integrations.zencal_client import ZencalClient


@pytest.mark.skipif(not os.getenv("ZENCAL_API_KEY"), reason="Brak ZENCAL_API_KEY w środowisku")
def test_zencal_get_events_live():
    client = ZencalClient(api_key=os.getenv("ZENCAL_API_KEY"))
    events = client.get_events()
    assert isinstance(events, list), "Zencal nie zwrócił listy wydarzeń (live)"
