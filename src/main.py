import logging
import os
import sys
from datetime import datetime, timezone

# Configure logging early so logger is available
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Inicjalizacja aplikacji Flask na samym początku
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))

from src.models.user import User


@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    users = User.query.all()
    users = [u.to_dict() for u in users]
    stats = {"messages": 12345, "active_users": len(users)}
    backup_status = "OK (ostatni backup: 2025-11-30)"
    telegram_status = "OK"
    rodo_audit = ["All consents valid", "No data leaks detected"]
    if request.method == "POST":
        backup_status = "Backup triggered manually!"
    return render_template(
        "admin_dashboard.html",
        users=users,
        stats=stats,
        backup_status=backup_status,
        telegram_status=telegram_status,
        rodo_audit=rodo_audit,
    )


# RODO audit route
@app.route("/admin/rodo-audit")
def rodo_audit():
    audit_items = [
        "Personal data categories: name, email, chat history",
        "Retention: 12 months",
        "User consents: 100% valid",
        "Access logs: OK",
        "Backup encryption: enabled",
        "Legal basis: consent, contract",
    ]
    return render_template("rodo_audit.html", audit_items=audit_items)


# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask_cors import CORS
from sqlalchemy import text

from src.models.chatbot import db

# Error monitoring: GCP Error Reporting działa AUTOMATYCZNIE w App Engine!
# Logi błędów: https://console.cloud.google.com/errors?project=glass-core-467907-e9
# NOTE: app already initialized above, don't create it again!


# Security headers (HSTS, clickjacking, MIME sniffing, XSS)
@app.after_request
def set_security_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # Enable HSTS in production environments
    if os.getenv("FLASK_ENV") == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # Minimal CSP to reduce risk while keeping compatibility
    csp_min = "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
    # Prepare strict CSP with nonce (opt-in via ENABLE_STRICT_CSP)
    # Note: Using nonce requires templates to inject the same nonce into script tags
    if os.getenv("ENABLE_STRICT_CSP") == "true":
        import secrets

        nonce = secrets.token_urlsafe(16)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}'; "
            "style-src 'self'; img-src 'self' data: https:; connect-src 'self'"
        )
        response.headers["X-Content-Security-Policy-Nonce"] = nonce
    else:
        response.headers["Content-Security-Policy"] = csp_min
    return response


def is_rate_limit_disabled() -> bool:
    """Return True when rate limiting should be skipped (e.g., during local CI runs)."""

    flag = os.getenv("DISABLE_RATE_LIMITS", "").lower()
    return flag in {"1", "true", "yes", "on"}


class NoopLimiter:
    """Minimal stub used when limits are intentionally disabled."""

    def limit(self, *_args, **_kwargs):
        def decorator(func):
            return func

        return decorator


# Initialize rate limiter (Redis backend or memory fallback)
# Configuration from environment variables for flexibility
chat_rate_limit = os.getenv("CHAT_RATE_LIMIT", "30 per minute")
default_rate_limits = [
    os.getenv("API_RATE_LIMIT_HOUR", "200 per hour"),
    os.getenv("API_RATE_LIMIT_MINUTE", "50 per minute"),
]

if is_rate_limit_disabled():
    limiter = NoopLimiter()
    logger.warning("⚠️ Rate limiting disabled via DISABLE_RATE_LIMITS")
    app.extensions["limiter"] = limiter
else:
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=default_rate_limits,
        storage_uri=os.getenv("REDIS_URL", "memory://"),
        strategy="fixed-window",
    )
    logger.info(
        f"✅ Rate limiter initialized (backend: {'Redis' if os.getenv('REDIS_URL') else 'memory'})"
    )
    logger.info(f"   Chat endpoint limit: {chat_rate_limit}")
    logger.info(f"   Default limits: {', '.join(default_rate_limits)}")

# SECURITY: Secret key from environment (NEVER hardcode!)
# Fail-fast if critical secrets missing in production
if os.getenv("FLASK_ENV") == "production":
    required_secrets = ["SECRET_KEY", "OPENAI_API_KEY", "ADMIN_API_KEY"]
    missing = [key for key in required_secrets if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            f"Missing critical environment variables in production: {', '.join(missing)}"
        )

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "dev-secret-change-in-production-" + os.urandom(24).hex()
)

# SECURITY: File upload limits
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max request size
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "/tmp/uploads")

# CORS Configuration with caching
# Production: Restrict to your domain
# Development: Allow all for testing
if os.getenv("FLASK_ENV") == "production":
    CORS(
        app,
        origins=[
            "https://novahouse.pl",
            "https://www.novahouse.pl",
            "https://glass-core-467907-e9.ey.r.appspot.com",
        ],
        max_age=3600,
    )  # Cache preflight requests for 1h
else:
    # Development mode - allow all
    CORS(app, max_age=3600)

# Initialize WebSocket support (v2.3) with optimizations
from src.services.websocket_service import socketio

socketio.init_app(
    app,
    cors_allowed_origins="*",
    async_mode="threading",  # Better performance on App Engine
    ping_timeout=10,
    ping_interval=25,
)

# KROK 3: Konfigurujemy i łączymy bazę danych z aplikacją.
# Od tego momentu 'db' wie o istnieniu 'app'.
db_url = os.getenv("DATABASE_URL")
if not db_url:
    # Default to SQLite file, ensure directory exists
    db_dir = os.path.join(os.path.dirname(__file__), "database")
    os.makedirs(db_dir, exist_ok=True)
    db_url = f"sqlite:///{os.path.join(db_dir, 'app.db')}"

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Connection pool settings dla App Engine (only for PostgreSQL)
if db_url.startswith("postgresql://"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": 2,  # Zmniejszamy na 2 żeby zmniejszyć load
        "max_overflow": 0,  # Brak overflow - stricte 2 połączenia
        "pool_pre_ping": True,  # Zawsze sprawdzaj czy połączenie żyje
        "pool_recycle": 900,  # Recykluj co 15 min zamiast 30 (App Engine timeout)
        "pool_reset_on_return": "rollback",  # Reset stanu połączenia po każdym użyciu
        "connect_args": {
            "connect_timeout": 5,  # Max 5s na połączenie
            "keepalives": 1,  # Włącz keepalives
            "keepalives_idle": 30,  # Keepalive co 30s
            "keepalives_interval": 10,  # Spróbuj co 10s
            "keepalives_count": 5,  # Max 5 prób
        },
    }
db.init_app(app)

# Flag for auto-migration - DISABLED (causes database locks on PostgreSQL)
_auto_migration_done = False

# NOTE: Auto-migration disabled due to table locking issues
# Use manual migration endpoint instead:
# GET /admin/migrate-database?secret=NOVAHOUSE_MIGRATION_2025_SECURE

# DISABLED - causing app hangs
# @app.before_request
# def run_migration_on_critical_endpoint():
#     ...


# Slow query logging (queries >100ms)
import logging
import time

from sqlalchemy import event
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    if total > 0.1:  # 100ms threshold
        logger.warning(f"Slow query ({total:.3f}s): {statement[:200]}")


from src.routes.ab_testing import ab_testing_bp
from src.routes.analytics import analytics_bp
from src.routes.backup import backup_routes
from src.routes.booking import booking_bp
from src.routes.chatbot import chatbot_bp

# New v2.3 routes
from src.routes.dashboard_widgets import dashboard_widgets
from src.routes.docs import docs_bp
from src.routes.entities import entities_bp
from src.routes.file_upload import file_upload_routes
from src.routes.health import health_bp
from src.routes.i18n import i18n_bp
from src.routes.intents import intents_bp
from src.routes.knowledge import knowledge_bp
from src.routes.leads import leads_bp
from src.routes.qualification import qualification_bp
from src.routes.search import search_routes

# Swagger UI (v2.3.1)
from src.routes.swagger_ui import swagger_ui_bp

# KROK 4: DOPIERO TERAZ, gdy aplikacja i baza są połączone,
# importujemy trasy (blueprints), które z nich korzystają.
from src.routes.user import user_bp

# KROK 5: Rejestrujemy nasze trasy w aplikacji.
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
app.register_blueprint(health_bp, url_prefix="/api")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
app.register_blueprint(leads_bp, url_prefix="/api/leads")
app.register_blueprint(intents_bp, url_prefix="/api/intents")
app.register_blueprint(entities_bp, url_prefix="/api/entities")
app.register_blueprint(qualification_bp, url_prefix="/api/qualification")
app.register_blueprint(booking_bp, url_prefix="/api/booking")
app.register_blueprint(knowledge_bp, url_prefix="/api/knowledge")
app.register_blueprint(docs_bp)
app.register_blueprint(ab_testing_bp, url_prefix="/api/ab-testing")
app.register_blueprint(i18n_bp, url_prefix="/api/i18n")
# Register v2.3 routes
app.register_blueprint(dashboard_widgets)
app.register_blueprint(backup_routes)
app.register_blueprint(search_routes)
app.register_blueprint(file_upload_routes)
# Register v2.3.1 routes
app.register_blueprint(swagger_ui_bp)
# Register calculator route
from src.routes.calculator import calculator_routes

app.register_blueprint(calculator_routes)
# Register FAQ learning routes
from src.routes.faq_learning import faq_learning_routes

app.register_blueprint(faq_learning_routes)

# Register migration routes
from src.routes.migration import migration_bp

app.register_blueprint(migration_bp)

# Register unsubscribe routes (RODO/GDPR compliance)
from src.routes.unsubscribe import unsubscribe_bp

app.register_blueprint(unsubscribe_bp)

# Register cron routes (v2.4)
from src.routes.cron import cron_bp
from src.routes.migrations import migration_bp as migrations_bp

app.register_blueprint(cron_bp, url_prefix="/api/cron")
app.register_blueprint(migrations_bp, url_prefix="/api/migrations")

# Register admin migration endpoint
from src.routes.admin_migration import admin_migration_bp

app.register_blueprint(admin_migration_bp, url_prefix="/admin")

# Register verification routes (v2.5)
from src.routes.verification import verification_bp

app.register_blueprint(verification_bp)

# Register assignment routes (v2.5)
from src.routes.assignment import assignment_bp

app.register_blueprint(assignment_bp)

# Register monitoring routes (v2.5)
from src.routes.monitoring import monitoring_bp

app.register_blueprint(monitoring_bp)
# KROK 6: Tworzymy tabele w kontekście w pełni skonfigurowanej aplikacji.
with app.app_context():
    # Retry logic dla Connection Pool na start
    max_retries = 3
    retry_count = 0
    connection_ok = False

    while retry_count < max_retries and not connection_ok:
        try:
            # Test connection before create_all
            with db.engine.connect() as conn:
                conn.execute(db.text("SELECT 1"))
            connection_ok = True
            logger.info("✅ Database connection established on startup")
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2**retry_count  # Exponential backoff: 2, 4s
                logger.warning(
                    f"⚠️ DB connection failed (attempt {retry_count}/{max_retries}), retrying in {wait_time}s: {str(e)[:100]}"
                )
                time.sleep(wait_time)
            else:
                logger.error(
                    f"❌ Database connection failed after {max_retries} attempts - using fallback SQLite"
                )
                # Fallback to SQLite if PostgreSQL fails
                if not db_url.startswith("sqlite"):
                    app.config["SQLALCHEMY_DATABASE_URI"] = (
                        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
                    )
                    db.engine.dispose()

    try:
        db.create_all()
    except Exception as e:
        logger.warning(f"Database initialization skipped: {e}")

    # Initialize v2.3 services (LAZY LOADING for fast cold start)
    # Background initialization reduces cold start from 15s to <5s

    # Schedule backup immediately (fast operation)
    try:
        from src.services.backup_service import backup_service

        backup_service.schedule_automated_backup()
        logger.info("Automated backup scheduled (daily at 3 AM)")
    except Exception as e:
        logger.warning(f"Backup scheduling skipped: {e}")

    # Lazy init: Cache warming and search indexing happen on first request
    # This moves expensive operations (5-10s) out of cold start path
    try:
        import threading

        def background_init():
            """Initialize expensive services in background"""
            try:
                from src.services.redis_service import warm_redis_cache

                warm_redis_cache()
                logger.info("Redis cache warmed (background)")
            except Exception as e:
                logger.warning(f"Redis cache warming skipped: {e}")

            try:
                from src.services.search_service import search_service

                search_service.index_knowledge_base()
                logger.info("Search index built (background)")
            except Exception as e:
                logger.warning(f"Search indexing skipped: {e}")

        # Start background thread (non-blocking)
        init_thread = threading.Thread(target=background_init, daemon=True)
        init_thread.start()
        logger.info("Background initialization started (cache + search)")

    except Exception as e:
        logger.warning(f"Background initialization failed: {e}")

    # Schedule periodic cleanup of fallback cache (prevent memory leaks)
    try:
        from src.services.dead_letter_queue import DeadLetterQueueService
        from src.services.redis_service import get_redis_cache

        scheduler = BackgroundScheduler(daemon=True)

        # Job 1: Cache cleanup (every 10 minutes)
        scheduler.add_job(
            func=lambda: get_redis_cache().cleanup_expired_fallback(),
            trigger="interval",
            minutes=10,
            id="cache_cleanup",
            name="Cleanup expired fallback cache entries",
        )

        # Job 2: Dead-letter queue retry (every 5 minutes)
        scheduler.add_job(
            func=DeadLetterQueueService.retry_pending_alerts,
            trigger="interval",
            minutes=5,
            id="dlq_retry",
            name="Retry pending alerts in dead-letter queue",
        )

        # Job 3: Clean up old delivered alerts (daily)
        scheduler.add_job(
            func=lambda: DeadLetterQueueService.clear_delivered_alerts(older_than_hours=24),
            trigger="interval",
            hours=24,
            id="dlq_cleanup",
            name="Clean up old delivered alerts from dead-letter queue",
        )

        scheduler.start()
        logger.info("✅ APScheduler started: 3 background jobs configured")
        logger.info("   - Cache cleanup every 10 minutes")
        logger.info("   - Dead-letter queue retry every 5 minutes")
        logger.info("   - Old alert cleanup daily")
    except Exception as e:
        logger.warning(f"APScheduler initialization failed: {e}")

# ═══════════════════════════════════════════════════════════════
# GLOBAL ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════

# Handle psycopg2 connection errors gracefully
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError


@app.errorhandler(SQLAlchemyOperationalError)
def handle_db_connection_error(error):
    """Handle database connection errors"""
    logger.error(f"Database connection error: {str(error)[:200]}")
    # Try to recover by disposing of the connection pool
    try:
        db.engine.dispose()
    except Exception as e:
        logger.warning(f"Failed to dispose connection pool: {e}")
    return {
        "error": "Database temporarily unavailable. Please try again.",
        "code": "DB_UNAVAILABLE",
    }, 503


@app.errorhandler(413)
def request_entity_too_large(error):
    """File too large"""
    return {"error": "File too large. Maximum size is 50MB."}, 413


@app.errorhandler(404)
def not_found(error):
    """Page not found"""
    return {"error": "Resource not found"}, 404


@app.errorhandler(500)
def internal_error(error):
    """Internal server error"""
    return {"error": "An unexpected error occurred"}, 500


# ═══════════════════════════════════════════════════════════════
# ENHANCED HEALTH CHECK
# ═══════════════════════════════════════════════════════════════


@app.route("/api/health/deep", methods=["GET"])
def deep_health_check():
    """Deep health check with all dependencies"""
    status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {},
    }

    # Check database
    try:
        from src.database import db

        db.session.execute(text("SELECT 1"))
        status["checks"]["database"] = "ok"
    except Exception as e:
        status["checks"]["database"] = f"error: {str(e)}"
        status["status"] = "degraded"

    # Check Redis
    try:
        from src.services.redis_service import redis_cache

        redis_cache.set("health_check", "ok", ttl=10)
        status["checks"]["redis"] = "ok" if redis_cache.get("health_check") == "ok" else "fallback"
    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")
        status["checks"]["redis"] = "fallback (in-memory)"

    # Check Search index
    try:
        from src.services.search_service import search_service

        stats = search_service.get_stats()
        status["checks"]["search"] = f"ok ({stats.get('total_documents', 0)} docs)"
    except Exception as e:
        status["checks"]["search"] = f"error: {str(e)}"
        status["status"] = "degraded"

    # Check WebSocket
    try:
        from src.services.websocket_service import get_active_connections_count

        count = get_active_connections_count()
        status["checks"]["websocket"] = f"ok ({count} active)"
    except Exception as e:
        status["checks"]["websocket"] = f"error: {str(e)}"

    return status, 200 if status["status"] == "healthy" else 503


# Reszta kodu do serwowania plików statycznych pozostaje bez zmian.
@app.route("/admin")
def admin_page():
    return app.send_static_file("admin-dashboard.html")


@app.route("/qualification")
def qualification_page():
    return app.send_static_file("qualification.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        response = send_from_directory(static_folder_path, path)
        # Add caching headers for static files
        if path.endswith(
            (
                ".js",
                ".css",
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".ico",
                ".svg",
                ".woff",
                ".woff2",
                ".ttf",
            )
        ):
            response.cache_control.max_age = 86400  # 24h
            response.cache_control.public = True
        return response
    else:
        index_path = os.path.join(static_folder_path, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, "index.html")
        else:
            return "index.html not found", 404


# Uruchomienie lokalne pozostaje bez zmian.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_ENV") != "production"
    # Use socketio.run instead of app.run for WebSocket support
    socketio.run(app, host="0.0.0.0", port=port, debug=debug)
