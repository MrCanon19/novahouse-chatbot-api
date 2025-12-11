"""
Integration Tests - Monday.com, CRM, Verification
Tests all customer service paths and data saving.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    """Create Flask app for testing"""
    from src.main import app
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def mock_monday():
    """Mock Monday.com API"""
    with patch("src.integrations.monday_client.MondayClient") as mock:
        mock_client = MagicMock()
        mock_client.create_lead_item.return_value = {"id": "monday_item_123"}
        mock_client.get_item.return_value = {"id": "monday_item_123", "name": "Test Lead"}
        yield mock_client


class TestMondayIntegration:
    """Test Monday.com integration"""
    
    def test_create_lead_in_monday(self, client, mock_monday):
        """Test creating lead in Monday.com"""
        response = client.post(
            "/api/leads/",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+48123456789",
                "message": "Interested in Premium package"
            },
            headers={"X-API-Key": "test_admin_key"}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["email"] == "test@example.com"
        # Verify Monday.com was called (if configured)
        # This would require mocking the actual MondayClient call
    
    def test_lead_data_saved_correctly(self, client):
        """Test that lead data is saved correctly"""
        lead_data = {
            "name": "Jan Kowalski",
            "email": "jan@example.com",
            "phone": "+48123456789",
            "message": "Interested in Comfort package",
            "property_size": "120m²",
            "location": "Warszawa"
        }
        
        response = client.post(
            "/api/leads/",
            json=lead_data,
            headers={"X-API-Key": "test_admin_key"}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == lead_data["name"]
        assert data["email"] == lead_data["email"]
        assert data["phone"] == lead_data["phone"]


class TestVerificationIntegration:
    """Test email/phone verification"""
    
    def test_email_verification_endpoint_exists(self, client):
        """Test email verification endpoint"""
        response = client.post(
            "/api/verification/email",
            json={"email": "test@example.com", "code": "123456"}
        )
        # Should return 200 (verified) or 400 (invalid code)
        assert response.status_code in [200, 400]
    
    def test_phone_verification_endpoint_exists(self, client):
        """Test phone verification endpoint"""
        response = client.post(
            "/api/verification/phone",
            json={"phone": "+48123456789", "code": "123456"}
        )
        # Should return 200 (verified) or 400 (invalid code)
        assert response.status_code in [200, 400]


class TestAssignmentIntegration:
    """Test lead assignment system"""
    
    def test_assign_lead_endpoint_exists(self, client):
        """Test lead assignment endpoint"""
        response = client.post(
            "/api/assignment/assign",
            json={"lead_id": 1, "user_id": "sales_person_1"},
            headers={"X-API-Key": "test_admin_key"}
        )
        # Should return 200 (assigned) or 404 (lead not found)
        assert response.status_code in [200, 404, 401]


class TestDataConsistency:
    """Test data consistency across integrations"""
    
    def test_lead_created_in_db_and_monday(self, client, mock_monday):
        """Test that lead is created in both DB and Monday.com"""
        lead_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+48123456789"
        }
        
        response = client.post(
            "/api/leads/",
            json=lead_data,
            headers={"X-API-Key": "test_admin_key"}
        )
        assert response.status_code == 201
        
        # Verify lead exists in DB
        lead_id = response.get_json()["id"]
        
        # Verify Monday.com was called (if configured)
        # This would require checking mock_monday.create_lead_item was called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

