def test_health_endpoint(client):
    response = client.get("/api/chatbot/health")
    assert response.status_code == 200


def test_status_endpoint(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    payload = response.get_json()

    assert payload["status"] == "healthy"
    assert payload["service"] == "novahouse-chatbot"
    assert payload["uptime_seconds"] >= 0
    assert payload["database"]["status"] == "connected"


def test_qualification_questions(client):
    response = client.get("/api/qualification/questions")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["questions"]) >= 7  # At least 7 questions


def test_leads_list(client):
    response = client.get("/api/leads/")
    assert response.status_code == 200
