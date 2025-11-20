import os
import traceback

import pytest


@pytest.mark.usefixtures("app")
def test_rodo_consent_and_export(app):
    client = app.test_client()

    # create consent
    resp = client.post(
        "/api/chatbot/rodo-consent", json={"session_id": "test-x", "consent_given": True}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("success") is True

    # export data (include admin header if ADMIN_API_KEY is set)
    headers = {}
    if os.getenv("ADMIN_API_KEY"):
        headers["X-ADMIN-API-KEY"] = os.getenv("ADMIN_API_KEY")
    resp2 = client.get("/api/chatbot/export-data/test-x", headers=headers)
    # Jeśli błąd, pokaż pełny traceback
    if resp2.status_code != 200:
        print(f"Export failed: {resp2.get_json()}")
        try:
            raise Exception(resp2.get_json())
        except Exception:
            traceback.print_exc()
    assert resp2.status_code == 200
    exported = resp2.get_json()
    assert exported["session_id"] == "test-x"
    assert "consent" in exported
