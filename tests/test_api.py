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


def test_status_endpoint_reports_version(client, monkeypatch):
    monkeypatch.setenv("RELEASE_REVISION", "")
    monkeypatch.setenv("COMMIT_SHA", "  ")
    monkeypatch.delenv("GAE_VERSION", raising=False)
    monkeypatch.delenv("GAE_SERVICE", raising=False)
    monkeypatch.setenv("K_REVISION", "kube-rev-123")

    response = client.get("/api/status")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["version"] == "kube-rev-123"


def test_status_endpoint_reports_environment(client, monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "  staging  ")
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("ENV", raising=False)

    response = client.get("/api/status")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["environment"] == "staging"


def test_qualification_questions(client):
    response = client.get("/api/qualification/questions")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["questions"]) >= 7  # At least 7 questions


def test_leads_list(client):
    response = client.get("/api/leads/")
    assert response.status_code == 200
