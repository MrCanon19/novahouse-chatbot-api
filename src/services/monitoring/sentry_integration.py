"""
Sentry Integration - Error tracking and monitoring
"""
import os
from typing import Optional


def init_sentry() -> Optional[object]:
    """
    Initialize Sentry for error tracking.
    
    Returns:
        Sentry SDK instance or None if not configured
    """
    sentry_dsn = os.getenv("SENTRY_DSN")
    
    if not sentry_dsn or sentry_dsn.lower() in ["", "none", "false"]:
        print("⚠️  Sentry DSN not configured - error tracking disabled")
        return None

    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                FlaskIntegration(transaction_style="endpoint"),
                SqlalchemyIntegration(),
            ],
            # Set traces_sample_rate to 1.0 to capture 100% of transactions
            # In production, use lower value (e.g., 0.1) to reduce performance impact
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
            # Set profiles_sample_rate to profile performance
            profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.0")),
            # Environment
            environment=os.getenv("FLASK_ENV", "production"),
            # Release version (from env or git)
            release=os.getenv("APP_VERSION", "unknown"),
            # Filter sensitive data
            before_send=lambda event, hint: _filter_sensitive_data(event),
        )

        print("✅ Sentry initialized successfully")
        return sentry_sdk

    except ImportError:
        print("⚠️  sentry-sdk not installed - install with: pip install sentry-sdk[flask]")
        return None
    except Exception as e:
        print(f"❌ Failed to initialize Sentry: {e}")
        return None


def _filter_sensitive_data(event: dict) -> Optional[dict]:
    """
    Filter sensitive data from Sentry events.
    
    Args:
        event: Sentry event dictionary
        
    Returns:
        Filtered event or None to drop event
    """
    # Remove sensitive data from request data
    if "request" in event and "data" in event["request"]:
        data = event["request"]["data"]
        
        # Mask emails
        if isinstance(data, dict):
            for key in list(data.keys()):
                if "email" in key.lower() or "mail" in key.lower():
                    data[key] = "[REDACTED]"
                if "phone" in key.lower() or "tel" in key.lower():
                    data[key] = "[REDACTED]"
                if "password" in key.lower() or "secret" in key.lower():
                    data[key] = "[REDACTED]"
        
        # Mask in JSON strings
        if isinstance(data, str):
            import re
            data = re.sub(r'(["\']email["\']\s*:\s*["\'])[^"\']+', r'\1[REDACTED]', data)
            data = re.sub(r'(["\']phone["\']\s*:\s*["\'])[^"\']+', r'\1[REDACTED]', data)
            event["request"]["data"] = data

    return event


def capture_exception(error: Exception, **kwargs):
    """Capture exception in Sentry"""
    try:
        import sentry_sdk
        sentry_sdk.capture_exception(error, **kwargs)
    except ImportError:
        pass  # Sentry not available


def capture_message(message: str, level: str = "info", **kwargs):
    """Capture message in Sentry"""
    try:
        import sentry_sdk
        sentry_sdk.capture_message(message, level=level, **kwargs)
    except ImportError:
        pass  # Sentry not available


def set_user_context(user_id: Optional[str] = None, email: Optional[str] = None):
    """Set user context in Sentry"""
    try:
        import sentry_sdk
        sentry_sdk.set_user({
            "id": user_id,
            "email": email[:3] + "***" if email else None,  # Mask email
        })
    except ImportError:
        pass  # Sentry not available

