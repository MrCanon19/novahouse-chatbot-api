# NovaHouse Chatbot API - AI Agent Instructions

## Architecture Overview

**Type:** Flask-based REST API chatbot for real estate finishing packages
**Deployment:** Google App Engine (Python 3.11+), with Docker support
**Database:** PostgreSQL (production) / SQLite (local)
**Entry Point:** `main.py` → imports `src/main.py` (Flask app)

### Core Components

- **`src/models/chatbot.py`**: SQLAlchemy models (Intent, Entity, Conversation, Lead, ChatMessage, etc.)
- **`src/routes/`**: Flask Blueprints for all endpoints (chatbot, leads, analytics, booking, etc.)
- **`src/knowledge/novahouse_info.py`**: Hardcoded business data (packages, FAQ, contact info) - 900+ lines
- **`src/services/`**: Rate limiting, auto-migration, file uploads, notifications
- **`src/integrations/`**: Monday.com, Booksy, Twilio, GCS integrations

### Key Patterns

1. **Blueprint Architecture**: All routes are Flask Blueprints registered in `src/main.py` (~464 lines)
   ```python
   from src.routes.chatbot import chatbot_bp
   app.register_blueprint(chatbot_bp)
   ```

2. **Lazy Loading**: OpenAI client loaded on first use to optimize cold starts
   ```python
   def get_openai_client():  # in src/routes/chatbot.py
       global _openai_client
       if _openai_client is None:
           _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
   ```

3. **Dual Database Support**: PostgreSQL (production) with SQLite fallback (local dev)
   - Connection pooling configured only for PostgreSQL (3 connections, 1 overflow)
   - Pool settings in `src/main.py` lines 144-160

## Database & Migrations

**Critical Pattern**: Migration system uses **manual HTTP endpoints**, NOT Alembic auto-migration due to App Engine limitations.

### Migration Workflow

1. **Auto-migration disabled** in `src/main.py` (causes table locks on PostgreSQL)
2. **Use manual endpoints**:
   - `/admin/migrate-database?secret=MIGRATION_SECRET_2025` (one-time, requires secret)
   - `/api/migration/add-leads-columns` (requires `X-ADMIN-API-KEY` header)
   - `/api/migration/v24` (versioned migrations)

3. **Pattern for adding columns**:
   ```python
   # Always use IF NOT EXISTS for safety
   "ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE"
   # Never accept column names from user input (SQL injection risk)
   ```

4. **Migration files**: `migrations/*.py` scripts for reference, but executed via HTTP endpoints
5. **Alembic configured** (`config/alembic.ini`) but NOT used for production deploys

## Development Workflow

### Setup & Running

```bash
# Automated setup (creates venv, installs deps, copies .env)
python scripts/setup.py

# Manual setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp config/environments/.env.example .env
python main.py  # Runs on port 8080 (auto-detects if occupied)

# Docker (full stack: app + PostgreSQL + Redis)
docker-compose -f config/docker-compose.yml up -d
```

### Testing

```bash
make test          # pytest with coverage (htmlcov/index.html)
make test-fast     # pytest without coverage
make lint          # flake8 + black --check
make format        # black + isort + autoflake (auto-fixes code style)
```

**Test Structure**:
- Unit tests: `tests/test_*.py` (18 files including smoke_tests.py)
- Integration tests: `tests/integration/` (opt-in via workflow_dispatch)
- CI/CD: `.github/workflows/ci-cd.yml` (Python 3.12, runs on push/PR to main)

### Code Style

- **Black** formatter (line length 100)
- **isort** with black profile
- **autoflake** removes unused imports
- **Pre-commit hooks** available via `make setup-hooks`

## Configuration & Secrets

### Environment Files

- **`app.yaml.example`**: GCP App Engine template (DO NOT put real secrets)
- **`config/environments/.env.example`**: Local development template
- **Instance class**: MINIMUM F2 (256MB) - F1 crashes with 500 errors (see app.yaml line 2)

### Required Secrets

- `SECRET_KEY`: Flask session encryption
- `API_KEY`/`ADMIN_API_KEY`: Dashboard, backup, A/B testing access
- `DATABASE_URL`: PostgreSQL connection string (Cloud SQL proxy format for GCP)
- `OPENAI_API_KEY`: GPT chatbot responses
- `MONDAY_API_KEY`, `MONDAY_BOARD_ID`: CRM integration
- Optional: `REDIS_URL`, `TWILIO_*`, `GCS_BUCKET_NAME`

### Security Headers

Set in `src/main.py` after_request hook (lines 67-86):
- HSTS (production only)
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- CSP minimal (strict CSP via `ENABLE_STRICT_CSP=true`)

## Critical Conventions

### Rate Limiting

- **In-memory** rate limiter (`src/services/rate_limiter.py`) for development
- **Redis-based** for production (when `REDIS_URL` set)
- Pattern: 10 requests/60 seconds per session_id or IP

### Error Handling

- **GCP Error Reporting** works automatically in App Engine (no Sentry needed for GAE)
- Slow query logging: Queries >100ms logged (SQLAlchemy events in `src/main.py` lines 184-195)
- Custom error pages: 404, 413, 500 handlers in `src/main.py`

### Knowledge Base Pattern

Business data (packages, FAQ, pricing) is **hardcoded** in `src/knowledge/novahouse_info.py`:
- `FAQ`: 45+ Q&A pairs
- `PACKAGES`: 5 finishing packages (Express, Express+, Comfort, Premium, Individual)
- `CONTACT_INFO`, `COVERAGE_AREAS`, `TEAM_INFO`, etc.
- Helper functions: `get_package_description()`, `get_portfolio_list()`, etc.

**Why hardcoded?**: Fast cold starts, no DB queries for static data, version-controlled changes.

### File Uploads

- **GCS integration** when `USE_CLOUD_STORAGE=true` + `GCS_BUCKET_NAME` set
- **Local fallback** to `uploads/` directory
- **Auto-optimization**: Generates 3 sizes (thumbnail 150px, medium 800px, original)
- Pattern in `src/routes/file_upload.py` with rate limiting decorator

## Deployment

### Google App Engine

```bash
# Via CI/CD (recommended)
git push origin main  # Triggers GitHub Actions deploy

# Manual deploy
gcloud app deploy app.yaml --project=glass-core-467907-e9

# Post-deploy smoke tests
python tests/smoke_tests.py https://glass-core-467907-e9.ey.r.appspot.com
```

### Health Checks

- `/api/health`: Basic health (always 200)
- `/api/health/deep`: Database + Redis connectivity check

## Common Pitfalls

1. **Don't use F1 instance class** - causes OOM crashes (see app.yaml line 2)
2. **Never run auto-migration on startup** - causes table locks in production
3. **Always use `IF NOT EXISTS`** in ALTER TABLE statements
4. **Don't put secrets in app.yaml** - use Secret Manager or secure vault
5. **Cold start optimization**: Avoid importing heavy libraries at module level (use lazy loading)
6. **PostgreSQL pool settings**: Keep pool_size=3, max_overflow=1 for App Engine

## Key Files Reference

- **Main entry**: `main.py` → `src/main.py` (Flask app init)
- **Models**: `src/models/chatbot.py` (360 lines), `src/models/user.py`, `src/models/analytics.py`
- **Core routes**: `src/routes/chatbot.py` (2814 lines - main chat logic)
- **Makefile**: 200+ lines with dev commands (test, lint, format, docker, deploy)
- **README.md**: 269 lines - comprehensive project docs
- **pyproject.toml**: Dependencies, pytest config, project metadata

## Documentation

- **Main**: `docs/README.md` - central documentation hub
- **Features**: `docs/features/` - Docker, enterprise features, backups
- **Guides**: `docs/guides/` - deployment, GCP setup, security
- **Status**: `docs/status/` - audit reports, session updates

## Local AI Setup (Ollama + Continue)

**Configured for:** Qwen2.5-coder:7b (4.7GB, 100% local, no API costs)

This project is pre-configured for local AI assistance:
- ✅ Config: `.vscode/continue_config.json`
- ✅ Full guide: `docs/guides/LOCAL_AI_SETUP.md`
- ✅ Model: `ollama run qwen2.5-coder:7b`

**Quick test:** `ollama list` should show `qwen2.5-coder:7b`

## Context Providers (Continue.dev)

### Quick Navigation for AI Assistants

**Most important files for understanding this codebase:**

1. **Entry points**: `main.py` → `src/main.py` (464 lines, Flask app initialization)
2. **Core logic**: `src/routes/chatbot.py` (2814 lines, main chat processing with GPT)
3. **Models**: `src/models/chatbot.py` (360 lines, SQLAlchemy models)
4. **Knowledge base**: `src/knowledge/novahouse_info.py` (929 lines, hardcoded FAQ/packages)
5. **Configuration**: `app.yaml.example`, `pyproject.toml`, `Makefile`

### Context Queries

When analyzing this project, use these queries:

- **"How does chat work?"** → Read `src/routes/chatbot.py` lines 1-150 (OpenAI integration)
- **"What are the packages?"** → Read `src/knowledge/novahouse_info.py` lines 100-400
- **"How to add a new route?"** → Check existing Blueprints in `src/routes/` + registration in `src/main.py`
- **"Database schema?"** → Read all models in `src/models/*.py`
- **"Migration pattern?"** → Read `src/routes/admin_migration.py` (HTTP-based, not Alembic)
- **"Testing approach?"** → Check `tests/conftest.py` + any `test_*.py` file

### Directory Structure Reference

```
src/
├── routes/          # 28+ Flask Blueprints (chatbot, leads, analytics, etc.)
├── models/          # SQLAlchemy models (chatbot.py, user.py, analytics.py)
├── knowledge/       # Hardcoded business data (novahouse_info.py - 929 lines)
├── services/        # Rate limiting, auto-migration, notifications
├── integrations/    # Monday.com, Booksy, Twilio, GCS
└── main.py          # Flask app init, Blueprint registration, DB config

tests/               # 18 test files (pytest, coverage)
migrations/          # Reference scripts (use HTTP endpoints instead)
docs/                # Extensive documentation (100+ MD files)
config/              # docker-compose.yml, alembic.ini, .env.example
```

### Common Tasks

**Add a new API endpoint:**
1. Create Blueprint in `src/routes/your_feature.py`
2. Register in `src/main.py`: `app.register_blueprint(your_bp)`
3. Add tests in `tests/test_your_feature.py`

**Add a new FAQ:**
1. Edit `src/knowledge/novahouse_info.py` → `FAQ` list
2. No migration needed (hardcoded data)

**Database migration:**
1. Create migration function in `src/routes/migration.py`
2. Use `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`
3. Deploy via HTTP endpoint (not auto-migration)

## Version History

- **v2.3.1** (current): Performance & Testing (18 automated tests, CI/CD, Redis)
- **v2.3.0**: Sentry monitoring, file uploads, WebSocket support
- **v2.2.0**: Advanced analytics, A/B testing, search engine
- **v1.0.0**: Core chatbot with 17 FAQ, 5 packages
