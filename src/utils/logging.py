"""
Structured JSON Logging with Request Tracking
Production-ready logging with request IDs, timestamps, and context
"""

import logging
import json
import uuid
from datetime import datetime
from flask import request, g, has_request_context
import sys
import os


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for easy parsing by log aggregators"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add request context if available
        if has_request_context():
            log_data["request"] = {
                "request_id": getattr(g, "request_id", None),
                "method": request.method,
                "path": request.path,
                "remote_addr": request.remote_addr,
                "user_agent": request.headers.get("User-Agent", ""),
            }

            # Add user info if authenticated
            if hasattr(g, "user"):
                log_data["user"] = {"id": g.user.id if g.user else None}

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        # Add extra fields
        if hasattr(record, "extra"):
            log_data["extra"] = record.extra

        # Add environment
        log_data["environment"] = os.getenv("FLASK_ENV", "production")

        return json.dumps(log_data)


class ConsoleFormatter(logging.Formatter):
    """Human-readable formatter for development"""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        # Add color if terminal supports it
        if sys.stderr.isatty():
            levelname = f"{self.COLORS.get(record.levelname, '')}{record.levelname}{self.RESET}"
        else:
            levelname = record.levelname

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        # Build message
        message = f"[{timestamp}] {levelname:8} {record.name}: {record.getMessage()}"

        # Add request ID if available
        if has_request_context() and hasattr(g, "request_id"):
            message += f" [req_id={g.request_id[:8]}]"

        # Add exception if present
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"

        return message


def setup_logging(app):
    """Configure application logging"""

    # Determine log format
    log_format = os.getenv("LOG_FORMAT", "json").lower()
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Create formatter
    if log_format == "json":
        formatter = JSONFormatter()
    else:
        formatter = ConsoleFormatter()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    root_logger.handlers = []

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Configure Flask app logger
    app.logger.setLevel(log_level)
    app.logger.handlers = []
    app.logger.addHandler(console_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)

    app.logger.info(f"Logging configured: level={log_level}, format={log_format}")


def add_request_id():
    """Middleware to add unique request ID to each request"""
    if not has_request_context():
        return

    # Generate or extract request ID
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        request_id = str(uuid.uuid4())

    g.request_id = request_id


def log_request(response):
    """Log each request with timing and status"""
    if not has_request_context():
        return response

    # Calculate request duration
    if hasattr(g, "request_start_time"):
        duration = (datetime.utcnow() - g.request_start_time).total_seconds() * 1000
    else:
        duration = 0

    # Log request
    logging.info(
        f"{request.method} {request.path} {response.status_code} {duration:.2f}ms",
        extra={
            "request_id": getattr(g, "request_id", None),
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": duration,
            "ip": request.remote_addr,
            "user_agent": request.headers.get("User-Agent", ""),
        },
    )

    # Add request ID to response headers
    if hasattr(g, "request_id"):
        response.headers["X-Request-ID"] = g.request_id

    return response


def setup_request_logging(app):
    """Setup request/response logging middleware"""

    @app.before_request
    def before_request():
        g.request_start_time = datetime.utcnow()
        add_request_id()

    @app.after_request
    def after_request(response):
        return log_request(response)

    @app.errorhandler(Exception)
    def log_exception(e):
        logging.error(
            f"Unhandled exception: {str(e)}",
            exc_info=True,
            extra={
                "request_id": getattr(g, "request_id", None),
                "method": request.method if has_request_context() else None,
                "path": request.path if has_request_context() else None,
            },
        )
        raise


# Convenience functions for structured logging
def log_event(event_name, **kwargs):
    """Log a structured event"""
    logging.info(f"Event: {event_name}", extra={"event": event_name, **kwargs})


def log_metric(metric_name, value, **kwargs):
    """Log a metric"""
    logging.info(
        f"Metric: {metric_name}={value}", extra={"metric": metric_name, "value": value, **kwargs}
    )
