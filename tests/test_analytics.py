#!/usr/bin/env python3
"""
Testy dla analytics endpoints
"""

import sys
import os

# Dodaj ścieżkę do głównego katalogu projektu
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app
import json

def test_analytics_overview():
    """Test endpoint /api/analytics/overview"""
    print("Testing /api/analytics/overview...")
    client = app.test_client()
    response = client.get('/api/analytics/overview?days=7')
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    assert 'status' in data, "Response should contain 'status'"
    assert data['status'] == 'success', f"Expected success status, got {data.get('status')}"
    assert 'overview' in data, "Response should contain 'overview'"
    
    print("✅ Analytics overview endpoint works!")
    return True

def test_analytics_conversations():
    """Test endpoint /api/analytics/conversations"""
    print("Testing /api/analytics/conversations...")
    client = app.test_client()
    response = client.get('/api/analytics/conversations?days=7')
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    assert 'status' in data, "Response should contain 'status'"
    assert data['status'] == 'success', f"Expected success status, got {data.get('status')}"
    
    print("✅ Analytics conversations endpoint works!")
    return True

def test_analytics_engagement():
    """Test endpoint /api/analytics/engagement"""
    print("Testing /api/analytics/engagement...")
    client = app.test_client()
    response = client.get('/api/analytics/engagement?days=7')
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    assert 'status' in data, "Response should contain 'status'"
    assert data['status'] == 'success', f"Expected success status, got {data.get('status')}"
    
    print("✅ Analytics engagement endpoint works!")
    return True

def test_analytics_intents():
    """Test endpoint /api/analytics/intents"""
    print("Testing /api/analytics/intents...")
    client = app.test_client()
    response = client.get('/api/analytics/intents?days=7')
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    assert 'status' in data, "Response should contain 'status'"
    assert data['status'] == 'success', f"Expected success status, got {data.get('status')}"
    
    print("✅ Analytics intents endpoint works!")
    return True

def test_analytics_performance():
    """Test endpoint /api/analytics/performance"""
    print("Testing /api/analytics/performance...")
    client = app.test_client()
    response = client.get('/api/analytics/performance?hours=24')
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    assert 'status' in data, "Response should contain 'status'"
    assert data['status'] == 'success', f"Expected success status, got {data.get('status')}"
    
    print("✅ Analytics performance endpoint works!")
    return True

def test_analytics_leads():
    """Test endpoint /api/analytics/leads"""
    print("Testing /api/analytics/leads...")
    client = app.test_client()
    response = client.get('/api/analytics/leads?days=7')
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    assert 'status' in data, "Response should contain 'status'"
    assert data['status'] == 'success', f"Expected success status, got {data.get('status')}"
    
    print("✅ Analytics leads endpoint works!")
    return True

def test_analytics_export():
    """Test endpoint /api/analytics/export"""
    print("Testing /api/analytics/export...")
    client = app.test_client()
    response = client.get('/api/analytics/export?type=overview&days=7')
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    assert 'status' in data, "Response should contain 'status'"
    assert data['status'] == 'success', f"Expected success status, got {data.get('status')}"
    
    print("✅ Analytics export endpoint works!")
    return True

def test_chatbot_with_analytics():
    """Test chatbot endpoint with analytics tracking"""
    print("Testing /api/chatbot/chat with analytics...")
    client = app.test_client()
    
    response = client.post('/api/chatbot/chat',
                          json={
                              'message': 'Cześć',
                              'session_id': 'test-session-123',
                              'user_id': 'test-user'
                          },
                          content_type='application/json')
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = json.loads(response.data)
    assert 'status' in data, "Response should contain 'status'"
    assert data['status'] == 'success', f"Expected success status, got {data.get('status')}"
    assert 'response' in data, "Response should contain 'response'"
    
    print("✅ Chatbot endpoint with analytics tracking works!")
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Running Analytics Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_analytics_overview,
        test_analytics_conversations,
        test_analytics_engagement,
        test_analytics_intents,
        test_analytics_performance,
        test_analytics_leads,
        test_analytics_export,
        test_chatbot_with_analytics
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} test(s) failed!")
        sys.exit(1)