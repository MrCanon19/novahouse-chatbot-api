import pytest
import sys
sys.path.insert(0, 'src')

def test_health_endpoint():
    from main import app
    client = app.test_client()
    response = client.get('/api/chatbot/health')
    assert response.status_code == 200

def test_qualification_questions():
    from main import app
    client = app.test_client()
    response = client.get('/api/qualification/questions')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['questions']) == 7

def test_leads_list():
    from main import app
    client = app.test_client()
    response = client.get('/api/leads/')
    assert response.status_code == 200
