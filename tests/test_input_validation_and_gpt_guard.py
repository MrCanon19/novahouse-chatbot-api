import json

from src.routes import chatbot
from src.services.context_validator import ContextValidator
from src.services.message_handler import MessageHandler


class TestInputValidation:
    def test_invalid_email_not_saved(self, client, app):
        session = "validation-1"
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Mój email to zly@@example", "session_id": session},
        )
        assert response.status_code in [200, 400]

        with app.app_context():
            from src.models.chatbot import ChatConversation

            conv = ChatConversation.query.filter_by(session_id=session).first()
            assert conv is not None
            context = json.loads(conv.context_data or "{}")
            assert "email" not in context  # invalid email rejected

    def test_context_validator_rejects_numeric_name(self):
        is_valid, sanitized, error = ContextValidator.validate_name("12345")
        assert not is_valid
        assert sanitized is None
        assert error == "Name must contain letters"

    def test_city_validation_normalizes(self):
        valid, value, error = ContextValidator.validate_city("warszawa")
        assert valid
        assert value == "Warszawa"
        assert error is None or "accepted" in error.lower()


class TestGptGuard:
    def test_ensure_openai_client_skips_placeholder(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test_placeholder_key")
        monkeypatch.setenv("GPT_FALLBACK_ENABLED", "true")
        chatbot.openai_client = None  # reset lazy singleton
        client = chatbot.ensure_openai_client()
        assert client is None

    def test_message_handler_gpt_rate_limit(self, monkeypatch):
        mh = MessageHandler()
        # Force strict limit for test
        mh._gpt_calls_per_window = 1
        mh._gpt_call_window_sec = 60

        allowed_first = mh._allow_gpt_call("sess-rl-1")
        allowed_second = mh._allow_gpt_call("sess-rl-1")

        assert allowed_first is True
        assert allowed_second is False  # second call blocked in same window
