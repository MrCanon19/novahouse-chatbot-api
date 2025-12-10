"""
Pytest configuration and shared fixtures
"""

import os
import sys

import pytest

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


from src.models.chatbot import (  # Dodaj tu inne modele jeśli są
    AuditLog,
    ChatConversation,
    ChatMessage,
    Lead,
    RodoConsent,
    db,
)


@pytest.fixture(scope="session")
def app():
    import logging

    logging.basicConfig(level=logging.INFO)
    """Create application for testing"""
    # Set testing environment variables BEFORE importing app
    os.environ["TESTING"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
    os.environ["RATE_LIMIT_ENABLED"] = "false"  # Disable rate limiting in tests
    # Mock secrets to avoid accidental prod usage
    os.environ.setdefault("API_KEY", "test_api_key")
    os.environ.setdefault("ADMIN_API_KEY", "test_admin_api_key")
    os.environ.setdefault("OPENAI_API_KEY", "test_openai_key")
    os.environ.setdefault("MONDAY_API_KEY", "test_monday_key")

    # Import all models to ensure all tables/columns are created
    from src.main import app as flask_app

    # db już zaimportowany wyżej, nie powtarzamy importu

    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.config["WTF_CSRF_ENABLED"] = False

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        # Loguj listę kolumn w chat_conversations
        from sqlalchemy import inspect

        inspector = inspect(db.engine)
        columns = [col["name"] for col in inspector.get_columns("chat_conversations")]
        print(f"Kolumny chat_conversations: {columns}")
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()
