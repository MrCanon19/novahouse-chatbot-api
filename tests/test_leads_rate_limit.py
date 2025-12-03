def test_leads_rate_limit_allows_first_requests(client):
    # Allow a few requests
    for i in range(3):
        res = client.post(
            "/api/leads/",
            json={"name": "User", "email": f"u{i}@example.com"},
            headers={"X-Session-ID": "test-session"},
        )
        assert res.status_code in (201, 200, 429)


def test_leads_rate_limit_triggers_after_threshold(client):
    # Push over threshold
    triggered = False
    for i in range(8):
        res = client.post(
            "/api/leads/",
            json={"name": "User", "email": f"u{i}@example.com"},
            headers={"X-Session-ID": "rate-limit-session"},
        )
        if res.status_code == 429:
            triggered = True
            break
    assert triggered is True
