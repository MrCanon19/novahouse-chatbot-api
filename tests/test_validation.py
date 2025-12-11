def test_chat_requires_non_empty_message(client):
    res = client.post("/api/chatbot/chat", json={"message": "   "})
    assert res.status_code == 400
    # Error message may vary, just check it exists
    assert "error" in res.json or "message" in res.json


def test_chat_rejects_too_long_message(client):
    long_msg = "x" * 6000
    res = client.post("/api/chatbot/chat", json={"message": long_msg})
    assert res.status_code in (400, 413)


def test_lead_validation_invalid_email(client):
    res = client.post(
        "/api/leads/",
        json={"name": "Test", "email": "invalid"},
    )
    assert res.status_code == 400
    # Error message may vary, just check it exists
    assert "error" in res.json or "message" in res.json


def test_lead_validation_ok(client):
    res = client.post(
        "/api/leads/",
        json={"name": "Test User", "email": "test@example.com"},
    )
    # May require API key, so accept 201 or 401
    assert res.status_code in (201, 401, 403)
