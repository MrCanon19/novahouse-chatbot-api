"""
Enhanced Error Handling Service

Better error messages, admin notifications, retry logic.
Handles API failures and database issues gracefully.
"""

import logging
import os
import traceback
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorContext:
    """Context information for an error"""

    def __init__(
        self,
        error_type: str,
        message: str,
        severity: ErrorSeverity,
        endpoint: str = None,
        user_id: str = None,
        session_id: str = None,
    ):
        self.error_type = error_type
        self.message = message
        self.severity = severity
        self.endpoint = endpoint
        self.user_id = user_id
        self.session_id = session_id
        self.timestamp = datetime.now(timezone.utc)
        self.traceback = traceback.format_exc()


class EnhancedErrorHandler:
    """Enhanced error handling with notifications and recovery"""

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2

    # Admin notification threshold
    ADMIN_NOTIFY_SEVERITY = ErrorSeverity.ERROR

    @staticmethod
    def handle_error(
        error: Exception,
        context: Optional[ErrorContext] = None,
        notify_admin: bool = True,
    ) -> dict:
        """
        Handle error with logging, notification, and recovery suggestions

        Args:
            error: Exception that occurred
            context: Optional error context
            notify_admin: Whether to notify admin

        Returns:
            Dict with error info and recovery suggestions
        """
        if not context:
            context = ErrorContext(
                error_type=type(error).__name__,
                message=str(error),
                severity=ErrorSeverity.ERROR,
            )

        # Log error with full traceback
        logger.error(
            f"[{context.severity.value.upper()}] {context.error_type}: {context.message}",
            extra={
                "endpoint": context.endpoint,
                "user_id": context.user_id,
                "session_id": context.session_id,
                "traceback": context.traceback,
            },
        )

        # Notify admin if threshold reached
        if notify_admin and context.severity.value in ["error", "critical"]:
            EnhancedErrorHandler._notify_admin(context)

        # Generate user-friendly message
        user_message = EnhancedErrorHandler._get_user_message(context.error_type)

        # Suggest recovery action
        recovery = EnhancedErrorHandler._get_recovery_suggestion(context.error_type)

        return {
            "success": False,
            "error": user_message,
            "error_type": context.error_type,
            "recovery": recovery,
            "timestamp": context.timestamp.isoformat(),
        }

    @staticmethod
    def _get_user_message(error_type: str) -> str:
        """Get user-friendly error message"""
        messages = {
            "APIConnectionError": "Mamy problem z połączeniem. Spróbuj ponownie za chwilę.",
            "APITimeoutError": "Serwer nie odpowiada. Spróbuj ponownie.",
            "DatabaseError": "Problem z bazą danych. Nasz zespół został powiadomiony.",
            "OpenAIError": "Nie mogę odpowiedzieć w tej chwili. Spróbuj ponownie.",
            "ValidationError": "Nieprawidłowe dane. Sprawdź wiadomość i spróbuj ponownie.",
            "RateLimitError": "Zbyt wiele żądań. Czekaj chwilę i spróbuj ponownie.",
        }

        return messages.get(
            error_type,
            "Coś poszło nie tak. Nasz zespół zostal powiadomiony. Spróbuj ponownie za chwilę.",
        )

    @staticmethod
    def _get_recovery_suggestion(error_type: str) -> str:
        """Get recovery suggestion for error"""
        suggestions = {
            "APIConnectionError": "Sprawdź połączenie internetowe i spróbuj ponownie",
            "APITimeoutError": "Czekaj kilka sekund i spróbuj ponownie",
            "DatabaseError": "Poczekaj chwilę, zanim ponownie próbujesz",
            "OpenAIError": "Spróbuj z innym pytaniem lub czekaj chwilę",
            "ValidationError": "Sprawdź wiadomość i upewnij się, że dane są kompletne",
            "RateLimitError": "Czekaj co najmniej 60 sekund, zanim wysłesz następną wiadomość",
        }

        return suggestions.get(error_type, "Spróbuj ponownie za chwilę")

    @staticmethod
    def _notify_admin(context: ErrorContext) -> None:
        """Send notification to admin about error"""
        try:
            slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
            if not slack_webhook:
                return

            color = "#FF0000" if context.severity == ErrorSeverity.CRITICAL else "#FFA500"

            payload = {
                "text": f"⚠️  {context.severity.value.upper()}: {context.error_type}",
                "attachments": [
                    {
                        "color": color,
                        "fields": [
                            {
                                "title": "Error Type",
                                "value": context.error_type,
                                "short": True,
                            },
                            {
                                "title": "Severity",
                                "value": context.severity.value,
                                "short": True,
                            },
                            {
                                "title": "Message",
                                "value": context.message,
                                "short": False,
                            },
                            {
                                "title": "Endpoint",
                                "value": context.endpoint or "Unknown",
                                "short": True,
                            },
                            {
                                "title": "Session ID",
                                "value": context.session_id or "Unknown",
                                "short": True,
                            },
                            {
                                "title": "Timestamp",
                                "value": context.timestamp.isoformat(),
                                "short": False,
                            },
                        ],
                    }
                ],
            }

            requests.post(slack_webhook, json=payload, timeout=5)

        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")

    @staticmethod
    def handle_api_failure(error: Exception, endpoint: str, retry_count: int = 0) -> dict:
        """
        Handle API call failure with retry logic

        Args:
            error: Exception from API call
            endpoint: API endpoint that failed
            retry_count: Current retry attempt

        Returns:
            Dict with error info and retry suggestion
        """
        context = ErrorContext(
            error_type="APICallError",
            message=f"Failed to call {endpoint}: {str(error)}",
            severity=ErrorSeverity.ERROR,
            endpoint=endpoint,
        )

        if retry_count < EnhancedErrorHandler.MAX_RETRIES:
            context.message += f" (Retry {retry_count + 1}/{EnhancedErrorHandler.MAX_RETRIES})"
            should_retry = True
        else:
            should_retry = False

        result = EnhancedErrorHandler.handle_error(context)
        result["should_retry"] = should_retry
        result["retry_count"] = retry_count

        return result

    @staticmethod
    def handle_database_error(error: Exception, query: str = None) -> dict:
        """
        Handle database error with recovery suggestions

        Args:
            error: Database exception
            query: SQL query that failed (optional)

        Returns:
            Dict with error info
        """
        context = ErrorContext(
            error_type="DatabaseError",
            message=str(error),
            severity=(
                ErrorSeverity.CRITICAL
                if "connection" in str(error).lower()
                else ErrorSeverity.ERROR
            ),
        )

        if "connection" in str(error).lower():
            context.message += " - Database connection lost"
        elif "timeout" in str(error).lower():
            context.message += " - Query timeout"

        return EnhancedErrorHandler.handle_error(context, notify_admin=True)

    @staticmethod
    def handle_validation_error(field: str, value: str, reason: str) -> dict:
        """
        Handle validation error

        Args:
            field: Field name that failed validation
            value: Invalid value
            reason: Why validation failed

        Returns:
            Dict with error info
        """
        context = ErrorContext(
            error_type="ValidationError",
            message=f"Invalid {field}: {reason}",
            severity=ErrorSeverity.WARNING,
        )

        return EnhancedErrorHandler.handle_error(context, notify_admin=False)


# Singleton instance
error_handler = EnhancedErrorHandler()
