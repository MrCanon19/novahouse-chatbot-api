def test_health_endpoint(client):
    response = client.get("/api/chatbot/health")
    assert response.status_code == 200


def test_qualification_questions(client):
    response = client.get("/api/qualification/questions")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["questions"]) >= 7  # At least 7 questions


def test_leads_list(client):
    response = client.get("/api/leads/")
    assert response.status_code == 200
