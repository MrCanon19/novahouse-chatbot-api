"""
Tests for chatbot routes
"""

import pytest
from unittest.mock import patch, MagicMock
from src.models.chatbot import db, ChatConversation, ChatMessage


class TestChatbotHealth:
    """Tests for health check endpoint"""

    def test_health_check_returns_200(self, client):
        """Test that health check returns 200 OK"""
        response = client.get("/api/chatbot/health")
        assert response.status_code == 200

    def test_health_check_returns_json(self, client):
        """Test that health check returns JSON"""
        response = client.get("/api/chatbot/health")
        assert response.content_type == "application/json"

    def test_health_check_has_status(self, client):
        """Test that health check contains status field"""
        response = client.get("/api/chatbot/health")
        data = response.get_json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestChatEndpoint:
    """Tests for chat message endpoint"""

    def test_chat_requires_message(self, client):
        """Test that chat endpoint requires message field"""
        response = client.post("/api/chatbot/chat", json={})
        assert response.status_code == 400

    def test_chat_creates_conversation(self, client):
        """Test that chat creates new conversation"""
        with patch("src.routes.chatbot.genai") as mock_genai:
            mock_model = MagicMock()
            mock_model.generate_content.return_value.text = "Test response"
            mock_genai.GenerativeModel.return_value = mock_model

            response = client.post("/api/chatbot/chat", json={"message": "Hello"})

            assert response.status_code == 200
            data = response.get_json()
            assert "session_id" in data
            assert "response" in data

    def test_chat_saves_messages_to_db(self, client, app):
        """Test that chat saves messages to database"""
        with patch("src.routes.chatbot.genai") as mock_genai:
            mock_model = MagicMock()
            mock_model.generate_content.return_value.text = "Test response"
            mock_genai.GenerativeModel.return_value = mock_model

            client.post(
                "/api/chatbot/chat", json={"message": "Hello", "session_id": "test-session"}
            )

            with app.app_context():
                conv = ChatConversation.query.filter_by(session_id="test-session").first()
                assert conv is not None
                messages = ChatMessage.query.filter_by(conversation_id=conv.id).all()
                assert len(messages) == 2  # user + bot


class TestPackagesEndpoint:
    """Tests for packages knowledge endpoint"""

    def test_packages_returns_200(self, client):
        """Test that packages endpoint returns 200"""
        response = client.get("/api/knowledge/packages")
        assert response.status_code == 200

    def test_packages_returns_list(self, client):
        """Test that packages returns list of packages"""
        response = client.get("/api/knowledge/packages")
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_package_has_required_fields(self, client):
        """Test that each package has required fields"""
        response = client.get("/api/knowledge/packages")
        data = response.get_json()

        required_fields = ["name", "price_per_sqm", "standard", "ideal_for"]
        for package in data:
            for field in required_fields:
                assert field in package


class TestFAQEndpoint:
    """Tests for FAQ endpoint"""

    def test_faq_returns_200(self, client):
        """Test that FAQ endpoint returns 200"""
        response = client.get("/api/knowledge/faq")
        assert response.status_code == 200

    def test_faq_returns_dict(self, client):
        """Test that FAQ returns dictionary"""
        response = client.get("/api/knowledge/faq")
        data = response.get_json()
        assert isinstance(data, dict)
        assert len(data) > 0


class TestChatMessageProcessing:
    """Tests for chat message processing logic"""

    @patch("src.routes.chatbot.genai")
    def test_faq_detection(self, mock_genai, client):
        """Test that FAQ questions are detected"""
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Test response"
        mock_genai.GenerativeModel.return_value = mock_model

        response = client.post(
            "/api/chatbot/chat", json={"message": "Ile kosztuje pakiet express?"}
        )

        data = response.get_json()
        assert "response" in data
        assert len(data["response"]) > 0

    @patch("src.routes.chatbot.genai")
    def test_session_continuity(self, mock_genai, client):
        """Test that session maintains conversation continuity"""
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Test response"
        mock_genai.GenerativeModel.return_value = mock_model

        # First message
        response1 = client.post(
            "/api/chatbot/chat", json={"message": "Hello", "session_id": "test-123"}
        )
        data1 = response1.get_json()

        # Second message with same session
        response2 = client.post(
            "/api/chatbot/chat", json={"message": "Follow up", "session_id": "test-123"}
        )
        data2 = response2.get_json()

        assert data1["session_id"] == data2["session_id"]
        assert data1["conversation_id"] == data2["conversation_id"]
