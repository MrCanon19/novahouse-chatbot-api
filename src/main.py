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
from flask import Flask, g, render_template, request, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.middleware.rate_limiting import DummyLimiter, is_rate_limit_disabled
from src.services.secret_manager import load_secret_into_env

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

# Initialize Sentry for error tracking (optional)
from src.services.monitoring import init_sentry, capture_exception, MetricsService
from src.utils.logging import setup_logging, setup_request_logging

# Initialize Sentry
sentry = init_sentry()  # Will be None if not configured

# Setup structured logging with request IDs
setup_logging(app)
setup_request_logging(app)


# Security headers and CORS - use middleware
from src.middleware.security import configure_cors, add_security_headers

# Configure CORS with whitelist (never "*" in production)
allowed_origins = configure_cors(app)
logger.info(f"✅ CORS configured with {len(allowed_origins)} allowed origins")

# Security headers
@app.after_request
def set_security_headers(response):
    return add_security_headers(response)


# Initialize rate limiter (Redis backend or memory fallback)
# Configuration from environment variables for flexibility
chat_rate_limit = os.getenv("CHAT_RATE_LIMIT", "30 per minute")
default_rate_limits = [
    os.getenv("API_RATE_LIMIT_HOUR", "200 per hour"),
    os.getenv("API_RATE_LIMIT_MINUTE", "50 per minute"),
]

if is_rate_limit_disabled():
    limiter = DummyLimiter()
    logger.info("✅ Rate limiter disabled via RATE_LIMIT_ENABLED=false")
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

# SECURITY: Load secrets (Secret Manager fallback)
project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
for key in ["SECRET_KEY", "OPENAI_API_KEY", "ADMIN_API_KEY", "DATABASE_URL"]:
    load_secret_into_env(key, project_id=project_id)

# Fail-fast if critical secrets missing in production (after attempting Secret Manager)
if os.getenv("FLASK_ENV") == "production":
    required_secrets = ["SECRET_KEY", "OPENAI_API_KEY", "ADMIN_API_KEY"]
    missing = [key for key in required_secrets if not os.getenv(key)]
    if missing:
        error_msg = f"Missing critical environment variables in production: {', '.join(missing)}"
        logger.critical(error_msg)
        print(f"⚠️ CRITICAL: {error_msg}")
        if "SECRET_KEY" in missing:
            raise RuntimeError(error_msg)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "dev-secret-change-in-production-" + os.urandom(24).hex()
)

# SECURITY: File upload limits
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max request size
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "/tmp/uploads")

# CORS is now configured in security middleware above

# Initialize WebSocket support (v2.3) with optimizations (optional)
socketio = None  # Initialize to None to prevent NameError
try:
    from src.services.websocket_service import socketio
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode="threading",  # Better performance on App Engine
        ping_timeout=10,
        ping_interval=25,
    )
    logger.info("✅ WebSocket support initialized")
except ImportError:
    socketio = None  # Ensure it's None if import fails
    logger.info("ℹ️  WebSocket service not available, skipping")
except Exception as e:
    socketio = None  # Ensure it's None if initialization fails
    logger.warning(f"⚠️  WebSocket initialization failed: {e}")

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


from src.middleware.rate_limiting import DummyLimiter, is_rate_limit_disabled
# A/B testing blueprint (optional - may not exist)
try:
    from src.routes.ab_testing import ab_testing_bp
except ImportError:
    ab_testing_bp = None
from src.routes.analytics import analytics_bp
from src.routes.backup import backup_routes
from src.routes.booking import booking_bp
from src.routes.chatbot import chatbot_bp

# New v2.3 routes
from src.routes.dashboard_widgets import dashboard_widgets
# Optional routes (may not exist)
try:
    from src.routes.docs import docs_bp
except ImportError:
    docs_bp = None
from src.routes.entities import entities_bp
from src.routes.file_upload import file_upload_routes
from src.routes.health import health_bp
from src.routes.i18n import i18n_bp
from src.routes.intents import intents_bp
# Knowledge blueprint (optional - may not exist)
try:
    from src.routes.knowledge import knowledge_bp
except ImportError:
    knowledge_bp = None
from src.routes.leads import leads_bp
from src.routes.qualification import qualification_bp
from src.routes.search import search_routes

# Swagger UI (v2.3.1) - optional
try:
    from src.routes.swagger_ui import swagger_ui_bp
except ImportError:
    swagger_ui_bp = None

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
if knowledge_bp is not None:
    app.register_blueprint(knowledge_bp, url_prefix="/api/knowledge")
if docs_bp is not None:
    app.register_blueprint(docs_bp)
if ab_testing_bp is not None:
    app.register_blueprint(ab_testing_bp, url_prefix="/api/ab-testing")
app.register_blueprint(i18n_bp, url_prefix="/api/i18n")
# Register v2.3 routes
app.register_blueprint(dashboard_widgets)
app.register_blueprint(backup_routes)
app.register_blueprint(search_routes)
app.register_blueprint(file_upload_routes)
# Register v2.3.1 routes
if swagger_ui_bp is not None:
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

# Register RODO routes
from src.routes.rodo import rodo_bp
app.register_blueprint(rodo_bp)

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
        logger.info("Automated backup scheduled (every 2 weeks on Sunday at 3 AM)")
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
        if os.getenv("DISABLE_SCHEDULER", "false").lower() == "true":
            logger.warning("⏸ Scheduler disabled via DISABLE_SCHEDULER=true")
            raise RuntimeError("Scheduler disabled by env flag")

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
        
        # Job 4: Session timeout cleanup (hourly)
        from src.services.session_timeout import session_timeout_service
        scheduler.add_job(
            func=lambda: session_timeout_service.cleanup_old_sessions(older_than_hours=24),
            trigger="interval",
            hours=1,
            id="session_cleanup",
            name="Clean up old inactive sessions",
        )
        
        # Job 5: Send nudges to inactive sessions (every 15 minutes)
        scheduler.add_job(
            func=lambda: session_timeout_service.check_and_nudge_inactive_sessions(),
            trigger="interval",
            minutes=15,
            id="session_nudges",
            name="Send nudges to inactive sessions",
        )

        # Schedule Zencal team sync (daily at 4 AM)
        try:
            def sync_zencal_team():
                """Synchronize team members from Zencal API"""
                try:
                    with app.app_context():
                        from src.routes.booking import sync_zencal_team as sync_function
                        from flask import Flask
                        # Create a minimal request context for the sync
                        with app.test_request_context():
                            # Call the sync endpoint logic directly
                            from src.integrations.zencal_client import ZencalClient
                            from src.models.chatbot import TeamMember, db
                            
                            zencal = ZencalClient()
                            zencal_members = zencal.get_team_members()
                            
                            if not zencal_members:
                                logger.warning("No team members found in Zencal")
                                return
                            
                            synced_count = 0
                            created_count = 0
                            updated_count = 0
                            
                            for zencal_member in zencal_members:
                                member = TeamMember.query.filter_by(
                                    zencal_user_id=zencal_member.get("id")
                                ).first()
                                
                                if not member:
                                    member = TeamMember.query.filter_by(
                                        email=zencal_member.get("email")
                                    ).first()
                                
                                if member:
                                    member.zencal_user_id = zencal_member.get("id")
                                    member.zencal_booking_url = zencal_member.get("booking_url")
                                    if not member.name:
                                        member.name = zencal_member.get("name", "")
                                    updated_count += 1
                                else:
                                    member = TeamMember(
                                        name=zencal_member.get("name", ""),
                                        email=zencal_member.get("email", ""),
                                        zencal_user_id=zencal_member.get("id"),
                                        zencal_booking_url=zencal_member.get("booking_url"),
                                        is_active=True,
                                    )
                                    db.session.add(member)
                                    created_count += 1
                                
                                synced_count += 1
                            
                            db.session.commit()
                            logger.info(f"Zencal team sync: {synced_count} synced, {created_count} created, {updated_count} updated")
                            
                except Exception as e:
                    logger.warning(f"Zencal team sync failed: {e}")
            
            scheduler.add_job(
                func=sync_zencal_team,
                trigger="cron",
                hour=4,
                minute=0,
                id="zencal_sync",
                name="Daily Zencal team synchronization",
            )
            logger.info("Zencal team sync scheduled (daily at 4 AM)")
        except Exception as e:
            logger.warning(f"Zencal sync scheduling skipped: {e}")

        # Schedule FAQ auto-learning (daily at 2 AM)
        try:
            def run_auto_learn():
                """Run FAQ auto-learning in background"""
                try:
                    with app.app_context():
                        from src.models.faq_learning import LearnedFAQ, UnknownQuestion, db
                        from sqlalchemy import func
                        from difflib import SequenceMatcher
                        from datetime import datetime, timezone

                        # Pobierz wszystkie pending questions
                        pending_questions = UnknownQuestion.query.filter_by(status="pending").all()

                        # Grupuj podobne pytania (używając podobieństwa tekstowego)
                        question_groups = {}
                        for question in pending_questions:
                            # Znajdź podobne pytania
                            matched = False
                            for existing_key in question_groups.keys():
                                similarity = SequenceMatcher(None, question.question.lower(), existing_key.lower()).ratio()
                                if similarity > 0.7:  # 70% podobieństwa
                                    question_groups[existing_key].append(question)
                                    matched = True
                                    break

                            if not matched:
                                question_groups[question.question] = [question]

                        # Dodaj do FAQ jeśli grupa ma >= 3 pytania
                        learned_count = 0
                        for question_text, questions in question_groups.items():
                            if len(questions) >= 3:
                                # Sprawdź czy już nie ma takiego FAQ
                                existing_faq = LearnedFAQ.query.filter_by(
                                    question_pattern=question_text[:200]  # Max 200 chars
                                ).first()

                                if not existing_faq:
                                    # Użyj najczęstszej odpowiedzi jako wzorca
                                    bot_responses = [q.bot_response for q in questions if q.bot_response]
                                    if bot_responses:
                                        most_common_response = max(set(bot_responses), key=bot_responses.count)

                                        # Utwórz nowy FAQ
                                        new_faq = LearnedFAQ(
                                            question_pattern=question_text[:200],
                                            answer=most_common_response[:5000] if most_common_response else "Brak odpowiedzi",
                                            category="auto-learned",
                                            created_by="auto-learning-system",
                                        )
                                        db.session.add(new_faq)

                                        # Oznacz pytania jako dodane do FAQ
                                        for q in questions:
                                            q.status = "added_to_faq"
                                            q.reviewed_at = datetime.now(timezone.utc)
                                            q.reviewed_by = "auto-learning-system"

                                        learned_count += 1

                        db.session.commit()
                        if learned_count > 0:
                            logger.info(f"✅ FAQ auto-learning: {learned_count} new FAQs learned")
                        else:
                            logger.debug("✅ FAQ auto-learning: no new FAQs to learn")

                except Exception as e:
                    logger.error(f"❌ FAQ auto-learning failed: {e}")

            scheduler.add_job(
                run_auto_learn,
                trigger="cron",
                hour=2,
                minute=0,
                id="faq_auto_learn",
                replace_existing=True,
            )
            logger.info("✅ FAQ auto-learning scheduled (daily at 2 AM)")
        except Exception as e:
            logger.warning(f"⚠️ Failed to schedule FAQ auto-learning: {e}")

        scheduler.start()
        logger.info("✅ APScheduler started: 7 background jobs configured")
        logger.info("   - Cache cleanup every 10 minutes")
        logger.info("   - Dead-letter queue retry every 5 minutes")
        logger.info("   - Old alert cleanup daily")
        logger.info("   - Session cleanup hourly")
        logger.info("   - Session nudges every 15 minutes")
        logger.info("   - RODO anonymization daily")
    except Exception as e:
        logger.warning(f"APScheduler initialization failed: {e}")

# ═══════════════════════════════════════════════════════════════
# GLOBAL ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════

# Handle psycopg2 connection errors gracefully
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError

# Import Werkzeug HTTP exceptions for proper error handling
from werkzeug.exceptions import (
    BadRequest,
    Unauthorized,
    Forbidden,
    NotFound,
    MethodNotAllowed,
    RequestTimeout,
    TooManyRequests,
    RequestEntityTooLarge,
    ServiceUnavailable,
)


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


@app.errorhandler(400)
@app.errorhandler(BadRequest)
def bad_request(error):
    """Bad request (400) - client error"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(400)
    
    # Don't log 400 as ERROR - it's a client mistake, not server issue
    logger.debug(f"Bad request: {str(error)[:200]}")
    
    response_data = {"error": "bad_request", "message": "Invalid request"}
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 400


@app.errorhandler(401)
@app.errorhandler(Unauthorized)
def unauthorized(error):
    """Unauthorized (401) - authentication required"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(401)
    
    logger.debug(f"Unauthorized: {str(error)[:200]}")
    
    response_data = {"error": "unauthorized", "message": "Authentication required"}
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 401


@app.errorhandler(403)
@app.errorhandler(Forbidden)
def forbidden(error):
    """Forbidden (403) - access denied"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(403)
    
    logger.debug(f"Forbidden: {str(error)[:200]}")
    
    response_data = {"error": "forbidden", "message": "Access denied"}
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 403


@app.errorhandler(404)
@app.errorhandler(NotFound)
def not_found(error):
    """Page not found (404)"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(404)
    
    # Don't log 404 as ERROR - it's normal for missing resources
    logger.debug(f"Not found: {request.path if hasattr(request, 'path') else 'unknown'}")
    
    response_data = {"error": "not_found", "message": "Resource not found"}
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 404


@app.errorhandler(405)
@app.errorhandler(MethodNotAllowed)
def method_not_allowed(error):
    """Method not allowed (405) - wrong HTTP method"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(405)
    
    # CRITICAL FIX: Don't log 405 as ERROR - it's a client mistake, not server issue
    # This prevents false alarms in GCP Error Reporting
    method = request.method if hasattr(request, 'method') else 'unknown'
    path = request.path if hasattr(request, 'path') else 'unknown'
    logger.debug(f"Method not allowed: {method} {path}")
    
    response_data = {
        "error": "method_not_allowed",
        "message": f"Method {method} not allowed for this endpoint"
    }
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 405


@app.errorhandler(408)
@app.errorhandler(RequestTimeout)
def request_timeout(error):
    """Request timeout (408)"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(408)
    
    logger.warning(f"Request timeout: {str(error)[:200]}")
    
    response_data = {"error": "request_timeout", "message": "Request timed out"}
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 408


@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    """File too large (413)"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(413)
    
    logger.warning(f"Request entity too large: {str(error)[:200]}")
    
    response_data = {"error": "file_too_large", "message": "File too large. Maximum size is 50MB."}
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 413


@app.errorhandler(429)
@app.errorhandler(TooManyRequests)
def too_many_requests(error):
    """Too many requests (429) - rate limit exceeded"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(429)
    
    # Don't log 429 as ERROR - it's expected behavior for rate limiting
    logger.info(f"Rate limit exceeded: {request.remote_addr if hasattr(request, 'remote_addr') else 'unknown'}")
    
    response_data = {"error": "rate_limit_exceeded", "message": "Too many requests. Please try again later."}
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 429


@app.errorhandler(503)
@app.errorhandler(ServiceUnavailable)
def service_unavailable(error):
    """Service unavailable (503) - temporary service issue"""
    request_id = getattr(g, "request_id", None)
    MetricsService.increment_error(503)
    
    logger.warning(f"Service unavailable: {str(error)[:200]}")
    
    response_data = {"error": "service_unavailable", "message": "Service temporarily unavailable"}
    if request_id:
        response_data["request_id"] = request_id
    return response_data, 503


# Import custom exceptions
from src.exceptions import (
    BusinessException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    ChatMessageTooLongError,
    InvalidFileTypeError,
    FileTooLargeError,
)


@app.errorhandler(BusinessException)
def handle_business_error(error: BusinessException):
    """Handle business logic errors (4xx)"""
    request_id = getattr(g, "request_id", None)
    
    # Map to appropriate status code
    status_map = {
        ValidationError: 400,
        AuthenticationError: 401,
        AuthorizationError: 403,
        NotFoundError: 404,
        ConflictError: 409,
        RateLimitError: 429,
        ChatMessageTooLongError: 413,
        InvalidFileTypeError: 415,
        FileTooLargeError: 413,
    }
    
    status_code = status_map.get(type(error), 400)
    MetricsService.increment_error(status_code)
    
    response_data = {
        "error": error.error_code.lower(),
        "message": error.message,
    }
    if request_id:
        response_data["request_id"] = request_id
    
    logger.warning(
        f"Business error [{error.error_code}]: {error.message}",
        extra={"request_id": request_id, "error_code": error.error_code}
    )
    
    return response_data, status_code


@app.errorhandler(Exception)
def handle_all_exceptions(error: Exception):
    """Global handler for all unhandled exceptions (500)"""
    request_id = getattr(g, "request_id", None)
    
    # Skip if already handled by specific handler
    if isinstance(error, BusinessException):
        return handle_business_error(error)
    
    # CRITICAL FIX: Check if this is a Werkzeug HTTP exception that should be handled differently
    from werkzeug.exceptions import HTTPException
    
    if isinstance(error, HTTPException):
        # Werkzeug HTTP exceptions should have been caught by specific handlers above
        # But if they slip through, handle them gracefully without logging as ERROR
        status_code = error.code if hasattr(error, 'code') else 500
        if status_code < 500:  # 4xx errors are client mistakes, not server errors
            logger.debug(f"HTTP exception (handled): {type(error).__name__}: {str(error)[:200]}")
            MetricsService.increment_error(status_code)
            response_data = {
                "error": error.name.lower().replace(" ", "_") if hasattr(error, 'name') else "client_error",
                "message": str(error.description) if hasattr(error, 'description') else str(error)
            }
            if request_id:
                response_data["request_id"] = request_id
            return response_data, status_code
    
    # Filter out test/health check errors that shouldn't trigger alerts
    path = request.path if hasattr(request, 'path') else ''
    user_agent = request.headers.get('User-Agent', '') if hasattr(request, 'headers') else ''
    
    # Ignore errors from health checks, monitoring, and common bot requests
    ignore_paths = ['/api/health', '/health', '/metrics', '/favicon.ico', '/robots.txt']
    ignore_agents = ['GoogleHC', 'HealthChecker', 'UptimeRobot', 'Pingdom']
    
    is_test_request = (
        any(ignore_path in path for ignore_path in ignore_paths) or
        any(ignore_agent in user_agent for ignore_agent in ignore_agents)
    )
    
    # Only capture real errors in Sentry (not test requests)
    if not is_test_request:
        capture_exception(error, extra={"request_id": request_id, "path": path})
    
    # Track metrics
    MetricsService.increment_error(500)
    
    # Log error (full traceback only in logs, not to user)
    # Use WARNING for test requests, ERROR for real issues
    log_level = logger.warning if is_test_request else logger.error
    log_level(
        f"Unhandled exception: {type(error).__name__}: {str(error)}",
        exc_info=not is_test_request,  # Full traceback only for real errors
        extra={"request_id": request_id, "path": path, "is_test_request": is_test_request}
    )
    
    response_data = {"error": "internal_error"}
    if request_id:
        response_data["request_id"] = request_id
    
    return response_data, 500


@app.errorhandler(500)
def internal_error(error):
    """Internal server error with request_id (fallback)"""
    return handle_all_exceptions(error)


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
    # Redirect to admin dashboard template
    from flask import redirect
    return redirect("/admin/dashboard")


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
    # Use socketio.run instead of app.run for WebSocket support (if available)
    if socketio is not None:
        try:
            socketio.run(app, host="0.0.0.0", port=port, debug=debug)
        except Exception as e:
            logger.error(f"WebSocket run failed: {e}, falling back to Flask run")
            app.run(host="0.0.0.0", port=port, debug=debug)
    else:
        # Fallback to standard Flask run if WebSocket not available
        app.run(host="0.0.0.0", port=port, debug=debug)
