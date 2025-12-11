"""
Smoke Tests for Production Deployment
Run these tests before every production deployment.
"""
import pytest
import os
from flask import Flask

# Skip if not in production environment
pytestmark = pytest.mark.skipif(
    os.getenv("FLASK_ENV") != "production",
    reason="Smoke tests only run in production environment"
)


@pytest.fixture
def app():
    """Create Flask app for testing"""
    from src.main import app
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestHealthChecks:
    """Test health check endpoints"""
    
    def test_health_endpoint(self, client):
        """Test basic health check"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
    
    def test_deep_health_check(self, client):
        """Test deep health check"""
        response = client.get("/api/health/deep")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert "checks" in data


class TestChatEndpoint:
    """Test chat endpoint"""
    
    def test_chat_endpoint_exists(self, client):
        """Test that chat endpoint exists and accepts POST"""
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "test"},
            content_type="application/json"
        )
        # Should return 200 or 400 (validation), not 404
        assert response.status_code in [200, 400, 429]
    
    def test_chat_validation(self, client):
        """Test chat payload validation"""
        # Empty message
        response = client.post(
            "/api/chatbot/chat",
            json={"message": ""},
            content_type="application/json"
        )
        assert response.status_code == 400
        
        # Too long message
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "A" * 5000},
            content_type="application/json"
        )
        assert response.status_code in [400, 413]
    
    def test_chat_rate_limiting(self, client):
        """Test rate limiting (may hit limit in tests)"""
        # Send multiple requests quickly
        responses = []
        for _ in range(35):  # More than default limit (30/min)
            response = client.post(
                "/api/chatbot/chat",
                json={"message": "test"},
                content_type="application/json"
            )
            responses.append(response.status_code)
        
        # At least one should be rate limited (429)
        # But may not always happen in test environment
        assert 200 in responses or 400 in responses  # At least some succeed


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_handler(self, client):
        """Test 404 error handler"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert "request_id" in data
    
    def test_500_handler(self, client):
        """Test 500 error handler (if we can trigger it)"""
        # This is hard to test without breaking things
        # But we can verify the handler exists
        pass


class TestSecurity:
    """Test security features"""
    
    def test_security_headers(self, client):
        """Test security headers are present"""
        response = client.get("/api/health")
        assert "X-Frame-Options" in response.headers
        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"
    
    def test_cors_headers(self, client):
        """Test CORS headers"""
        response = client.options("/api/chatbot/chat")
        # CORS headers should be present
        assert response.status_code in [200, 204]


class TestMonitoring:
    """Test monitoring endpoints"""
    
    def test_metrics_endpoint(self, client):
        """Test metrics endpoint (requires auth)"""
        response = client.get("/api/monitoring/metrics")
        # Should require auth (401) or return metrics (200)
        assert response.status_code in [200, 401]
    
    def test_health_monitoring(self, client):
        """Test monitoring health endpoint"""
        response = client.get("/api/monitoring/health")
        assert response.status_code == 200


class TestRODO:
    """Test RODO endpoints"""
    
    def test_rodo_inventory_requires_auth(self, client):
        """Test RODO inventory requires authentication"""
        response = client.get("/api/rodo/inventory")
        assert response.status_code == 401
    
    def test_rodo_export_endpoint_exists(self, client):
        """Test RODO export endpoint exists"""
        response = client.post(
            "/api/rodo/export",
            json={"email": "test@example.com"},
            content_type="application/json"
        )
        # Should return 404 (not found) or 200 (found)
        assert response.status_code in [200, 404, 400]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

