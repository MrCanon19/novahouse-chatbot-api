#!/usr/bin/env python3
"""
Testy dla analytics endpoints
"""

import pytest
import json


def test_analytics_overview(client):
    """Test endpoint /api/analytics/overview"""
    print("Testing /api/analytics/overview...")
    response = client.get("/api/analytics/overview?days=7")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = json.loads(response.data)
    assert "status" in data, "Response should contain 'status'"
    assert data["status"] == "success", f"Expected success status, got {data.get('status')}"
    assert "overview" in data, "Response should contain 'overview'"

    print("✅ Analytics overview endpoint works!")
    return True


def test_analytics_conversations(client):
    """Test endpoint /api/analytics/conversations"""
    print("Testing /api/analytics/conversations...")
    response = client.get("/api/analytics/conversations?days=7")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = json.loads(response.data)
    assert "status" in data, "Response should contain 'status'"
    assert data["status"] == "success", f"Expected success status, got {data.get('status')}"

    print("✅ Analytics conversations endpoint works!")
    return True


def test_analytics_engagement(client):
    """Test endpoint /api/analytics/engagement"""
    print("Testing /api/analytics/engagement...")
    response = client.get("/api/analytics/engagement?days=7")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = json.loads(response.data)
    assert "status" in data, "Response should contain 'status'"
    assert data["status"] == "success", f"Expected success status, got {data.get('status')}"

    print("✅ Analytics engagement endpoint works!")
    return True


def test_analytics_intents(client):
    """Test endpoint /api/analytics/intents"""
    print("Testing /api/analytics/intents...")
    response = client.get("/api/analytics/intents?days=7")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = json.loads(response.data)
    assert "status" in data, "Response should contain 'status'"
    assert data["status"] == "success", f"Expected success status, got {data.get('status')}"

    print("✅ Analytics intents endpoint works!")
    return True


def test_analytics_performance(client):
    """Test endpoint /api/analytics/performance"""
    print("Testing /api/analytics/performance...")
    response = client.get("/api/analytics/performance?days=7")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = json.loads(response.data)
    assert "status" in data, "Response should contain 'status'"
    assert data["status"] == "success", f"Expected success status, got {data.get('status')}"

    print("✅ Analytics performance endpoint works!")
    return True


def test_analytics_leads(client):
    """Test endpoint /api/analytics/leads"""
    print("Testing /api/analytics/leads...")
    response = client.get("/api/analytics/leads?days=7")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = json.loads(response.data)
    assert "status" in data, "Response should contain 'status'"
    assert data["status"] == "success", f"Expected success status, got {data.get('status')}"

    print("✅ Analytics leads endpoint works!")
    return True


def test_analytics_export(client):
    """Test endpoint /api/analytics/export"""
    print("Testing /api/analytics/export...")
    response = client.get("/api/analytics/export?type=overview&days=7")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = json.loads(response.data)
    assert "status" in data, "Response should contain 'status'"
    assert data["status"] == "success", f"Expected success status, got {data.get('status')}"

    print("✅ Analytics export endpoint works!")
    return True


def test_chatbot_with_analytics(client):
    """Test chatbot endpoint with analytics tracking"""
    print("Testing /api/chatbot/chat with analytics...")

    response = client.post(
        "/api/chatbot/chat",
        json={"message": "Cześć", "session_id": "test-session-123", "user_id": "test-user"},
        content_type="application/json",
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = json.loads(response.data)
    assert "response" in data, "Response should contain 'response'"
    assert "session_id" in data, "Response should contain 'session_id'"

    print("✅ Chatbot endpoint with analytics tracking works!")
    return True
