"""
Security Middleware
Handles CORS, CSRF, security headers, and authentication for admin endpoints.
"""
import os
from functools import wraps
from typing import List, Optional

from flask import g, request, jsonify, session
from flask_cors import CORS


# Allowed origins (whitelist)
def get_allowed_origins() -> List[str]:
    """Get list of allowed CORS origins based on environment"""
    env_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
    
    if env_origins:
        # Parse comma-separated list from env
        return [origin.strip() for origin in env_origins.split(",") if origin.strip()]
    
    # Default origins based on environment
    if os.getenv("FLASK_ENV") == "production":
        return [
            "https://novahouse.pl",
            "https://www.novahouse.pl",
            "https://glass-core-467907-e9.ey.r.appspot.com",
        ]
    elif os.getenv("FLASK_ENV") == "staging":
        return [
            "https://staging.novahouse.pl",
            "https://glass-core-467907-e9.ey.r.appspot.com",
        ]
    else:
        # Development - allow localhost
        return [
            "http://localhost:3000",
            "http://localhost:5000",
            "http://localhost:8080",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5000",
            "http://127.0.0.1:8080",
        ]


def configure_cors(app):
    """
    Configure CORS with whitelist of allowed origins.
    Never uses "*" in production.
    """
    allowed_origins = get_allowed_origins()
    
    CORS(
        app,
        origins=allowed_origins,
        max_age=3600,  # Cache preflight requests for 1h
        allow_headers=["Content-Type", "Authorization", "X-API-Key", "X-Request-ID"],
        methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    )
    
    return allowed_origins


def add_security_headers(response):
    """
    Add security headers to all responses.
    This should be used as @app.after_request decorator.
    """
    # X-Frame-Options: prevent clickjacking
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    
    # X-Content-Type-Options: prevent MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # X-XSS-Protection: enable XSS filter
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Referrer-Policy: control referrer information
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # HSTS: force HTTPS in production
    if os.getenv("FLASK_ENV") == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )
    
    # Content-Security-Policy
    csp_min = (
        "default-src 'self'; "
        "img-src 'self' data: https:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; "
        "connect-src 'self'"
    )
    
    # Strict CSP (opt-in via ENABLE_STRICT_CSP)
    if os.getenv("ENABLE_STRICT_CSP") == "true":
        import secrets
        
        nonce = secrets.token_urlsafe(16)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}'; "
            "style-src 'self'; "
            "img-src 'self' data: https:; "
            "connect-src 'self'"
        )
        response.headers["X-Content-Security-Policy-Nonce"] = nonce
    else:
        response.headers["Content-Security-Policy"] = csp_min
    
    return response


def require_auth(f):
    """
    Decorator to require authentication for admin endpoints.
    Checks for ADMIN_API_KEY in headers or session.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key in headers (support multiple header names)
        api_key = (
            request.headers.get("X-API-Key") 
            or request.headers.get("X-API-KEY")
            or request.headers.get("X-ADMIN-API-KEY")
            or request.headers.get("Authorization")
        )
        
        if api_key:
            # Remove "Bearer " prefix if present
            if api_key.startswith("Bearer "):
                api_key = api_key[7:]
            
            expected_key = os.getenv("ADMIN_API_KEY")
            if expected_key and api_key == expected_key:
                g.authenticated = True
                return f(*args, **kwargs)
        
        # Check for session (for web panel)
        if session.get("authenticated"):
            g.authenticated = True
            return f(*args, **kwargs)
        
        # Not authenticated
        return jsonify({"error": "authentication_required", "message": "Authentication required"}), 401
    
    return decorated_function


def require_csrf(f):
    """
    Decorator to require CSRF token for state-changing operations.
    Only applies to requests with cookies (web panel), not pure API calls.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip CSRF for API calls (no cookies)
        if not request.cookies:
            return f(*args, **kwargs)
        
        # Require CSRF token for web panel requests
        csrf_token = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
        session_token = session.get("csrf_token")
        
        if not csrf_token or csrf_token != session_token:
            return jsonify({"error": "csrf_token_invalid", "message": "Invalid CSRF token"}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def generate_csrf_token():
    """Generate CSRF token and store in session"""
    import secrets
    
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    
    return session["csrf_token"]


def get_csrf_token():
    """Get CSRF token from session"""
    return session.get("csrf_token", "")


# Admin endpoints that require authentication
ADMIN_ENDPOINTS = [
    "/api/analytics",
    "/api/leads",
    "/api/leads/export",
    "/api/faq-learning",
    "/api/monitoring",
    "/admin",
]


def is_admin_endpoint(path: str) -> bool:
    """Check if path is an admin endpoint"""
    return any(path.startswith(endpoint) for endpoint in ADMIN_ENDPOINTS)
